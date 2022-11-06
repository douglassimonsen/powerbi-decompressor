import os
from .pyadomd.pyadomd import Pyadomd
import uuid
from . import parse_schema, initialization
import shutil
import jinja2
import pathlib
import logging
base_path = pathlib.Path(__file__).parent / "xmla"
xmls = {f[:-4]: jinja2.Template(open(base_path / f).read()) for f in os.listdir(base_path)}
logger = logging.getLogger()


class PowerBi:
    def __init__(self, source_path):
        self.source_path = source_path
        self.guid = str(uuid.uuid4())  # this is important to compare with values in SSAS since they return as str's (_get_ssas_dbs)
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

    def _get_ssas_dbs(self):
        query = 'SELECT [catalog_name] as [Database Name] FROM $SYSTEM.DBSCHEMA_CATALOGS'
        with Pyadomd(self.conn_str) as conn:
            return [x[0] for x in conn.cursor().execute(query).fetchall()]

    def load_image(self):
        if self.guid in self._get_ssas_dbs():
            logger.warning("This database has already been loaded")
            return
        with Pyadomd(self.conn_str) as conn:
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