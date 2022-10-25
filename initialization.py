from sys import path
import os
path.append("\\Program Files\\Microsoft.NET\\ADOMD.NET\\150")
from pyadomd import Pyadomd
import uuid
import subprocess
import psutil
import time


def _check_active(directory):
    try:
        port = int(open(os.path.join(directory, 'msmdsrv.port.txt'), 'r', encoding='utf-16-le').read().strip())
    except FileNotFoundError:
        return False, None

    CONN_STR = f"Provider=MSOLAP;Data Source=localhost:{port};"
    try:
        with Pyadomd(CONN_STR) as conn:
            conn.cursor().executeNonQuery("SELECT [catalog_name] as [Database Name] FROM $SYSTEM.DBSCHEMA_CATALOGS")
            return True, port
    except:
        return False, None


class AnalysisService:
    def __init__(self):
        self.port = None
        self.guid = None
        self.active = False
        self.temp_folder = fr'C:\Users\{os.getlogin()}\AppData\Local\Microsoft\Power BI Desktop\AnalysisServicesWorkspaces'
    
    def instance_name(self):
        return f"AnalysisServicesWorkspace_{self.guid}"

    def data_directory(self):
        return os.path.join(self.temp_folder, self.instance_name(), 'Data')

    def init(self):
        self.check_existing_process()
        if not self.active:
            self.create_environment()

    def check_existing_process(self):
        for f in os.listdir(self.temp_folder):
            active, port = _check_active(os.path.join(self.temp_folder, f, 'Data'))
            if active:
                self.active = active
                self.port = port
                self.guid = f.split('_')[-1]
                break
    
    def create_environment(self):
        # C:\Program Files\Microsoft Power BI Desktop\bin\Microsoft.PowerBI.Client.Windows.dll
        # AnalysisServiceProcess line 169
        def get_port():
            for p in psutil.process_iter():
                if p.name() != 'msmdsrv.exe':
                    continue
                return p.connections()[0].laddr.port

        self.guid = uuid.uuid4()
        os.makedirs(self.data_directory())
        command = [
            r'C:\Program Files\Microsoft Power BI Desktop\bin\msmdsrv.exe', 
            "-c", 
            "-n", 
            self.instance_name(), 
            "-s", 
            f'{self.data_directory()}'
        ]
        subprocess.Popen(command)  # running multiple times doesn't cause multiple processes, thank god
        port = get_port()
        self.active = True
        self.port = port
        with open(f'{self.data_directory()}\msmdsrv.port.txt', 'w', encoding='utf-16-le') as f:
            f.write(str(port))


    def __str__(self):
        return f'''
        active: {self.active}
        port: {self.port}
        guid: {self.guid}
        folder: {self.data_directory()}
        '''


if __name__ == '__main__':
    x = AnalysisService()
    x.init()
    print(x)