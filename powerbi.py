from sys import path

path.append("\\Program Files\\Microsoft.NET\\ADOMD.NET\\150")
import os
from pyadomd import Pyadomd
import uuid
import parse_schema
import shutil

xmls = {f[:-4]: open(f"xmla/{f}").read() for f in os.listdir("xmla")}
CONN_STR = "Provider=MSOLAP;Data Source=localhost:61324;Catalog=15dfc18a-0908-493c-8f21-8162ba250dab;"


class PowerBi:
    def __init__(self, source_path):
        self.source_path = source_path
        self.guid = uuid.uuid4()
        self.schema = None

    def load_image(self):
        with Pyadomd(CONN_STR) as conn:  # need to generate a random GUID
            return conn.cursor().executeXML(
                xmls["image_load"].format(guid=self.guid, source_path=self.source_path)
            )

    def save_image(self, target_path):
        shutil.copy(self.source_path, target_path)  # needs a PBIX to save the datamodel into
        with Pyadomd(CONN_STR) as conn:
            x = conn.cursor().executeXML(
                xmls["image_save"].format(guid=self.guid, target_path=target_path)
            )

    def read_schema(self):
        with Pyadomd(CONN_STR) as conn:
            schema = conn.cursor().executeXML(xmls["schema_query"])
        self.schema = parse_schema.main(schema)
        return self.schema
