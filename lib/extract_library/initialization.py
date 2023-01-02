import os

try:
    from .pyadomd.pyadomd import Pyadomd
except ImportError:
    from pyadomd.pyadomd import Pyadomd
import uuid
import subprocess
import psutil
import time
import pathlib
import jinja2
import shutil
import structlog
import atexit

logger = structlog.getLogger()

config = jinja2.Template(
    open(pathlib.Path(__file__).parent / "xmla/msmdsrv.ini").read()
)
load_test = open(pathlib.Path(__file__).parent / "xmla/image_save.xml").read()


def _delete_workspace(directory):
    # the directory points to the Data directory, but we really want the parent workspace folder
    try:
        shutil.rmtree(pathlib.Path(directory).parent)
    except PermissionError:
        logger.info("PermissionError", directory=pathlib.Path(directory).parent)
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


class _Cleanup:
    def __init__(self, temp_folder_path: str = None, port: int = None) -> None:
        self.temp_folder_path = temp_folder_path
        self.port = port
        atexit.register(self.delete_folder)

    def kill_ssas_instance(self):
        for p in psutil.process_iter():
            for c in p.connections():
                if c.status == "LISTEN" and c.laddr.port == self.port:
                    p.terminate()
                    for _ in range(10):
                        try:
                            status = p.status()
                        except psutil.NoSuchProcess:
                            return
                        if status == "terminated":
                            return
                        logger.debug("ssas proc", status=status)
                        time.sleep(1)

    def delete_folder(self):
        import shutil

        logger.info("deleting temp data", folder=self.temp_folder_path)
        self.kill_ssas_instance()

        shutil.rmtree(self.temp_folder_path, ignore_errors=True)


class AnalysisService:
    def __init__(self, temp_folder_path: str = None, persist: bool = True):
        self.port = None
        self.guid = None
        self.active = False
        self.persist = persist
        self.temp_folder_path = (
            temp_folder_path
            or pathlib.Path(__file__).parent / "AnalysisServicesWorkspaces"
        )
        self._bad_ports = set()

    def instance_name(self):
        return f"AnalysisServicesWorkspace_{self.guid}"

    def data_directory(self):
        return os.path.join(self.temp_folder_path, self.instance_name(), "Data")

    def init(self):
        self.check_existing_process()
        if not self.active:
            self.create_environment()
        logger.info("SSAS init complete")

    @staticmethod
    def valid_sku(port):
        logger.debug("Checking SKU", port=port)
        CONN_STR = f"Provider=MSOLAP;Data Source=localhost:{port};"
        try:
            with Pyadomd(CONN_STR) as conn:
                conn.cursor().executeXML(load_test)
            # nothing here because we know the load test will fail
        except Exception as e:
            error_type = str(e.Message)
            if (
                error_type
                != "ImageLoad/ImageSave commands supports loading/saving data for Excel, Power BI Desktop or Zip files. File extension can be only .XLS?, .PBIX or .ZIP."
            ):
                logger.warn("bad SSAS instance", port=port, error_type=error_type)
            return (
                error_type
                == "ImageLoad/ImageSave commands supports loading/saving data for Excel, Power BI Desktop or Zip files. File extension can be only .XLS?, .PBIX or .ZIP."
            )

    def check_existing_process(self):
        os.makedirs(
            self.temp_folder_path, exist_ok=True
        )  # If powerbi has never been opened here, it won't exist
        for f in os.listdir(self.temp_folder_path):
            active, port = _check_active(os.path.join(self.temp_folder_path, f, "Data"))
            if active:
                if not self.valid_sku(port):
                    self._bad_ports.add(port)
                    continue
                logger.info("ssas_port", port=port, state="previous_ssas")
                self.active = active
                self.port = port
                self.guid = f.split("_")[-1]
                break

    def init_data_directory(self):
        data_dir = self.data_directory()
        logger.debug("initializing_data_directory", directory=data_dir)
        os.makedirs(data_dir)
        with open(os.path.join(data_dir, "msmdsrv.ini"), "w") as f:
            f.write(
                config.render(
                    data_directory=data_dir,
                    certificate_directory=rf"C:\Users\{os.getlogin()}\AppData\Local\Microsoft\Power BI Desktop\CertifiedExtensions",
                )
            )

    def create_environment(self):
        # C:\Program Files\Microsoft Power BI Desktop\bin\Microsoft.PowerBI.Client.Windows.dll
        # AnalysisServiceProcess line 169
        def get_port():
            for _ in range(30):
                logger.debug("Trying to read port file")
                try:
                    return int(
                        open(
                            pathlib.Path(__file__).parent
                            / f"AnalysisServicesWorkspaces/AnalysisServicesWorkspace_{self.guid}/Data/msmdsrv.port.txt",
                            encoding="utf-16-le",
                        ).read()
                    )
                except FileNotFoundError:
                    time.sleep(1)
            else:
                raise FileNotFoundError

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
        logger.info("creating new ssas", persisting=self.persist)
        subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=self.persist
            and subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
        )  # running multiple times doesn't cause multiple processes, thank god
        port = get_port()
        self.active = True
        self.port = port
        for _ in range(30):
            if self.valid_sku(port):
                break
            time.sleep(1)
        else:
            raise ValueError(
                "Configuration loaded improperly, SSAS lacks proper image load/save functions"
            )

        if not self.persist:
            _Cleanup(
                temp_folder_path=os.path.join(
                    self.temp_folder_path, self.instance_name()
                ),
                port=self.port,
            )

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
        logger.info("killing_PID", pid=p.pid)
        try:
            p.terminate()
        except psutil.AccessDenied:
            logger.warning("Permission_Denied", pid=p.pid)


def find_current_servers():
    for p in psutil.process_iter():
        if p.name() != "msmdsrv.exe":
            continue
        logger.info(
            "current_ssas_server", name=p.name(), port=p.connections()[0].laddr.port
        )


if __name__ == "__main__":
    kill_current_servers()
    x = AnalysisService()
    x.init()
    # print(x)
