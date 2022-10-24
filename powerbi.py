from sys import path

path.append("\\Program Files\\Microsoft.NET\\ADOMD.NET\\150")
import os
from pyadomd import Pyadomd
import uuid
import parse_schema
import shutil
import initialization

xmls = {f[:-4]: open(f"xmla/{f}").read() for f in os.listdir("xmla")}


class PowerBi:
    def __init__(self, source_path):
        self.source_path = source_path
        self.guid = uuid.uuid4()
        self.schema = None
        self.AnalysisService = None
        self.conn_str = None
    
    def init_backend(self):
        env = initialization.AnalysisService()
        env.init()
        self.AnalysisService = env
        self.conn_str = f"Provider=MSOLAP;Data Source=localhost:{self.AnalysisService.port};"

    def load_image(self):
        with Pyadomd(self.conn_str) as conn:  # need to generate a random GUID
            return conn.cursor().executeXML(
                xmls["image_load"].format(guid=self.guid, source_path=self.source_path)
            )

    def save_image(self, target_path):
        shutil.copy(self.source_path, target_path)  # needs a PBIX to save the datamodel into
        with Pyadomd(self.conn_str) as conn:
            x = conn.cursor().executeXML(
                xmls["image_save"].format(guid=self.guid, target_path=target_path)
            )

    def read_schema(self):
        with Pyadomd(self.conn_str) as conn:
            schema = conn.cursor().executeXML(xmls["schema_query"])
        self.schema = parse_schema.main(schema)
        return self.schema
