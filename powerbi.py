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
        self.init_backend()
        self.load_image()

    def init_backend(self):
        env = initialization.AnalysisService()
        env.init()
        self.AnalysisService = env
        self.conn_str = f"Provider=MSOLAP;Data Source=localhost:{self.AnalysisService.port};"

    def load_image(self):
        with Pyadomd(self.conn_str) as conn:  # need to generate a random GUID
            conn.cursor().executeXML(
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
            schema = conn.cursor().executeXML(xmls["schema_query"].format(guid=self.guid))
        self.schema = parse_schema.parse_schema(schema)
        return self.schema

    def update_table(self, table_name):
        if not self.schema:
            self.read_schema()

        table_dict = {t['Name']: t['ID'] for t in self.schema['Table']}
        table_id = table_dict[table_name]
        with Pyadomd(self.conn_str) as conn:
            ret = conn.cursor().executeXML(xmls["refresh_object"].format(guid=self.guid, table_id=table_id))