from sys import path

path.append("\\Program Files\\Microsoft.NET\\ADOMD.NET\\150")
import os
from pyadomd import Pyadomd
import uuid
import parse_schema
import shutil
import initialization
import jinja2
import pathlib
base_path = pathlib.Path(__file__).parent / "xmla"
xmls = {f[:-4]: jinja2.Template(open(base_path / f).read()) for f in os.listdir(base_path)}


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
        self.table_dict = {t['Name']: t['ID'] for t in self.schema['Table']}
        return self.schema

    def get_table(self, table_name):
        with Pyadomd(self.conn_str) as conn:
            cur = conn.cursor()
            data = cur.execute(f"Evaluate '{table_name}'").fetchall()
            columns = [x.name.split('[')[1].split(']')[0] for x in cur.description]
            data = [dict(zip(columns, row)) for row in data]
        return data

    def update_tables(self, table_names=None):
        if not self.schema:
            self.read_schema()

        if isinstance(table_names, str):
            table_ids = [self.table_dict[table_names]]
        elif isinstance(table_names, list):
            table_ids = [self.table_dict[t] for t in table_names]
        elif table_names is None:
            table_ids = list(self.table_dict.values())
        else:
            raise TypeError("I don't understand the object: ", table_names)
        with Pyadomd(self.conn_str) as conn:
            return conn.cursor().executeXML(xmls["update_table"].render(guid=self.guid, table_ids=table_ids))

    def __str__(self):
        return f'''
            path: {self.source_path}
            backend: {self.AnalysisService}
        '''