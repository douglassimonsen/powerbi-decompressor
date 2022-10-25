from sys import path

path.append("\\Program Files\\Microsoft.NET\\ADOMD.NET\\150")
import os
from pyadomd import Pyadomd
import uuid
import parse_schema
import shutil
import initialization
import jinja2
xmls = {f[:-4]: jinja2.Template(open(f"xmla/{f}").read()) for f in os.listdir("xmla")}


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
                xmls["image_load"].render(guid=self.guid, source_path=self.source_path)
            )

    def save_image(self, target_path):
        shutil.copy(self.source_path, target_path)  # needs a PBIX to save the datamodel into
        with Pyadomd(self.conn_str) as conn:
            x = conn.cursor().executeXML(
                xmls["image_save"].render(guid=self.guid, target_path=target_path)
            )

    def read_schema(self):
        with Pyadomd(self.conn_str) as conn:
            schema = conn.cursor().executeXML(xmls["schema_query"].render(guid=self.guid))
        self.schema = parse_schema.parse_schema(schema)
        return self.schema

    def update_tables(self, table_names=None):
        if not self.schema:
            self.read_schema()

        table_dict = {t['Name']: t['ID'] for t in self.schema['Table']}
        if isinstance(table_names, str):
            table_ids = [table_dict[table_names]]
        elif isinstance(table_names, list):
            table_ids = [table_dict[t] for t in table_names]
        elif table_names is None:
            table_ids = list(table_dict.values())
        else:
            raise TypeError("I don't understand the object: ", table_names)

        with Pyadomd(self.conn_str) as conn:
            return conn.cursor().executeXML(xmls["update_table"].render(guid=self.guid, table_ids=table_ids))