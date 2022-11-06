import os
from .pyadomd.pyadomd import Pyadomd
import uuid
import subprocess
import psutil
import time
import pathlib
import jinja2
import shutil
import logging

logger = logging.getLogger()

config = jinja2.Template(
    open(pathlib.Path(__file__).parent / "xmla/msmdsrv.ini").read()
)


def _delete_workspace(directory):
    # the directory points to the Data directory, but we really want the parent workspace folder
    try:
        shutil.rmtree(pathlib.Path(directory).parent)
    except PermissionError:
        logger.info(f"Could not remove {pathlib.Path(directory).parent}")
        pass


def _check_active(directory):
    try:
        port = int(
            open(os.path.join(directory, "msmdsrv.port.txt"), "r", encoding="utf-16-le")
            .read()
            .strip()
        )
    except (FileNotFoundError, ValueError):
        _delete_workspace(directory)
        return False, None

    CONN_STR = f"Provider=MSOLAP;Data Source=localhost:{port};"
    try:
        with Pyadomd(CONN_STR) as conn:
            conn.cursor().executeNonQuery(
                "SELECT [catalog_name] as [Database Name] FROM $SYSTEM.DBSCHEMA_CATALOGS"
            )
            return True, port
    except:
        _delete_workspace(directory)
        return False, None


class AnalysisService:
    def __init__(self):
        self.port = None
        self.guid = None
        self.active = False
        self.temp_folder = fr"C:\Users\{os.getlogin()}\AppData\Local\Microsoft\Power BI Desktop\AnalysisServicesWorkspaces"

    def instance_name(self):
        return f"AnalysisServicesWorkspace_{self.guid}"

    def data_directory(self):
        return os.path.join(self.temp_folder, self.instance_name(), "Data")

    def init(self):
        self.check_existing_process()
        if not self.active:
            self.create_environment()

    def check_existing_process(self):
        for f in os.listdir(self.temp_folder):
            active, port = _check_active(os.path.join(self.temp_folder, f, "Data"))
            if active:
                self.active = active
                self.port = port
                self.guid = f.split("_")[-1]
                break

    def init_data_directory(self):
        data_dir = self.data_directory()
        os.makedirs(data_dir)
        with open(os.path.join(data_dir, "msmdsrv.ini"), "w") as f:
            f.write(config.render(data_directory=data_dir))

    def create_environment(self):
        # C:\Program Files\Microsoft Power BI Desktop\bin\Microsoft.PowerBI.Client.Windows.dll
        # AnalysisServiceProcess line 169
        def get_port():
            for p in psutil.process_iter():
                if p.name() != "msmdsrv.exe":
                    continue
                for _ in range(5):
                    conns = p.connections()
                    if len(conns) == 0:
                        print("sleep 2")
                        time.sleep(2)
                        continue
                    print("Port:", conns[0].laddr.port)
                    return conns[0].laddr.port

        self.guid = uuid.uuid4()
        self.init_data_directory()
        command = [
            r"C:\Program Files\Microsoft Power BI Desktop\bin\msmdsrv.exe",
            "-c",
            "-n",
            self.instance_name(),
            "-s",
            f"{self.data_directory()}",
        ]
        subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )  # running multiple times doesn't cause multiple processes, thank god
        port = get_port()
        self.active = True
        self.port = port
        with open(
            f"{self.data_directory()}\msmdsrv.port.txt", "w", encoding="utf-16-le"
        ) as f:
            f.write(str(port))

    def __str__(self):
        return f"""
        active: {self.active}
        port: {self.port}
        guid: {self.guid}
        folder: {self.data_directory()}
        """


def kill_current_servers():
    for p in psutil.process_iter():
        if p.name() != "msmdsrv.exe":
            continue
        p.terminate()
        print("Killing PID", p.pid)


def find_current_servers():
    for p in psutil.process_iter():
        if p.name() != "msmdsrv.exe":
            continue
        print(f"{p.name()} at {p.connections()[0].laddr.port}")


if __name__ == "__main__":
    kill_current_servers()
    x = AnalysisService()
    x.init()
    print(x)
