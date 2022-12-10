import lark
from pprint import pprint
import zlib
import base64
import functools


l = lark.Lark(
    """
    start: line*
    line: "let" | "in" | statement | variable
    statement: variable "=" command

    command: (function | source_filter) ","?
    function: /[\w\.]+/ "(" (function | arg) ("," (function | arg))* ")"
    arg: /[^\(\)]+/

    source_filter: variable "{[" (sf_var ","?)* "]}[Data]"
    sf_var: no_space_variable "=" "\\"" no_space_variable "\\""

    variable: no_space_variable | space_variable
    no_space_variable: /[\w_]+/
    space_variable: /#"[\w ]+"/
    %import common.WS
    %ignore WS
"""
)


def decompress_static(raw):
    y = base64.b64decode(raw)
    decompress = zlib.decompressobj(-zlib.MAX_WBITS)
    z = decompress.decompress(y)
    z += decompress.flush()
    return z.decode("utf-8")


class Sources(lark.Transformer):
    def __init__(self):
        self.sources = []

    def arg(self, args):
        return args[0].value

    def function(self, args):
        f = {
            "func": args[0].value,
            "args": args[1:],
            "type": "function",
        }
        return f

    def source_filter(self, args):
        return {
            "var": args[0],
            "args": dict(x.children for x in args[1:]),
            "type": "source_filter",
        }

    def command(self, args):  # command is just a convenience around two values
        return args[0]

    def no_space_variable(self, args):
        return args[0].value

    def space_variable(self, args):
        return args[0].value

    def variable(self, args):
        return args[0]

    def statement(self, args):
        return {
            "var": args[0],
            "expr": args[1],
        }

    def line(self, args):
        if len(args) == 0:
            return None
        args = args[0]
        if isinstance(args, str):  # variable
            args = {"var": args}
        return args

    def start(self, lines):
        self.sources = []
        lines = [x for x in lines if x is not None]
        func_type = lines[0].get("expr", {}).get("func")
        if func_type == "Excel.Workbook":
            self.sources.append(
                {
                    "type": "Excel.Workbook",
                    "path": lines[0]["expr"]["args"][0]["args"][0].strip('"'),
                    "sheet": lines[1].get("expr", {}).get("args", {}).get("Item"),
                }
            )
        elif func_type == "Csv.Document":
            self.sources.append(
                {
                    "type": "Csv.Document",
                    "path": lines[0]["expr"]["args"][0]["args"][0].strip('"'),
                }
            )
        elif func_type == "Sql.Database":
            if isinstance(lines[0]["expr"]["args"], list):
                self.sources.append(
                    {
                        "type": "Sql.Database",
                        "Query": lines[0].get("expr", {}).get("args", [None])[-1],
                    }
                )

            else:
                self.sources.append(
                    {
                        "type": "Sql.Database",
                        "Table": lines[1].get("expr", {}).get("args", {}).get("Item"),
                        "Schema": lines[1]
                        .get("expr", {})
                        .get("args", {})
                        .get("Schema"),
                    }
                )
        elif func_type in (
            "Table.ExpandTableColumn",  # this appears to just be existing tables
            "Table.AddIndexColumn",
            "Table.NestedJoin",
            "Table.SelectColumns",
        ):
            pass
        elif func_type == "Table.FromRows":
            static_data = None
            if lines[0]["expr"]["args"][0].get("func") == "Json.Document":
                if (
                    lines[0]["expr"]["args"][0]["args"][0].get("func")
                    == "Binary.Decompress"
                ):
                    if (
                        lines[0]["expr"]["args"][0]["args"][0]["args"][0].get("func")
                        == "Binary.FromText"
                    ):
                        static_data = decompress_static(
                            lines[0]["expr"]["args"][0]["args"][0]["args"][0]["args"][
                                0
                            ].split('"')[1]
                        )

            self.sources.append({"Type": "Json.Document", "static_data": static_data})
        return self.sources


_s = Sources()


# this function is one of the slowest in the codebase and one that is likely to have repeated inputs
@functools.cache
def get_sources(query_definition):
    query_definition = [
        y.strip()
        for y in query_definition.splitlines()
        if y.strip() not in ("let", "in")
    ]
    query_definition = "\n".join(query_definition[:2])

    ret = _s.transform(l.parse(query_definition))
    try:
        ret = _s.transform(l.parse(query_definition))
    except (lark.exceptions.UnexpectedCharacters, lark.exceptions.UnexpectedEOF):
        ret = []
    return ret


if __name__ == "__main__":
    x = r"""let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("XVVdb9w2EPwrBz/HBD+Wy93HIkYbN7VdtGmMIvCDfKf4iDtLhqSL4/76LrmU4xbwg3UaUrOzO7Nfvpz9dOzuu8fu7N1Z8IYsYnLy/zmhSexcsPKA8uLs7l3FzocCRWdCsslhgbroDVgAx/Lk0aBip/zPONR7g0meU+QKds5AcN6Xr6A1oYEP3TB3c0GDYeRkoaDZy3cEHRQMFfy+O+av4zTkejka59DboJezQXIRy+HIK348jlO3GwuajY1MrpbobDRB+NRPQTSuoYeh3y55e1rKz85ETol8OZC8STGGKhBwRV/0x+65m3q9OziKlet5iiaKPlCgMbYqL/K8THm7bMavGyF1erzXEsgQJwhUDyZjvdSQykHXdP9ZCsi7gvXJJESfqpbkpFpMVL6YrEkV+0s/Tg+56W7BolNsMAjBplIrBhMr9oNwz7lc64xlaQtpP5MBphBSvbciL3fdvggIYLz0eu0lGEhEnvSNyn15POZhzKWXIP0FhpgqAzJM6MJ/KrscdrnTKWFDgvXYps9H8okUq5Vdjs8FCN5Y52KoFDgYL32spyC1Sz++zhIZeYXWVqhMtEegAo3QWvKxH5bT9vBSwMmgCA8VTGAwWYtJ+6cj/dt4yvNK1xmHHKHSZSlH+mBjERebDlddHnoVBjkwVBFQhoQc+1Rnq+Gml2M37Np4okDrpQnFjlKcU76+gee52+5Pc78ss4rhg3Xq2STDKg+2iaETepW3+/zQDeW3YILIoV2WCmNAy/Ft766yDP88Lp06AhkgQtOZrRXi6olGJs9z+Xt6yhofCRwqeRIjJkJGHTd4xY+nKWtnIKKl2FzuiQKSVqpiX43DolIDGvby6agzJzEQIcSg1etoXPf3U4smYee8mFR7TkbMZKt9gdp4XPfful0zXnAhunaxOK+4u6YBN/Wu++fNh+7xad7nanKREKIH9qveGKgWKS/o9cSv/TT3L2oAz8QaZkkUL/2sDf3B/Hlz1X/P21Gzj8CuhKyYAAgq+bhqWPB/j9NBq3cYkzpGLmeQCXTauQYep2W/ed9No1iyViw9DTLWeoRL3mtsR35z4KI7tBFIwpjY1WqZTRJ29QHWLL7Z57EZnUiT6JykNgSuVcQ1lm4OR0mQx0YiYgzgmyu5fCJpYmvvb6b+YRx0MKVA6zWvvTg/Wa5BKd1UBr/3wzC/HL91ug+ESWSbom9h6q1snvi2/X/sx12/uZyb56CEqCUOa0dlEMgqdTXon+PpfypKryOSDgFZET5am3RRwpsjP3QU+zK3LSI6Sta30IzNSp/6Yry571WfJLEKsSUhsg/1QXIZG/q75pvEdgSgGi2cyjQC1sUKrdi/lm6vqjjhGPy6ggk9BFBZ9M7P/fQollO2kvCUcN15Mok1NWXgdEw+Z1kxbf+WhcS6K84TlVBkNfK6UG87Mc/wsGhDZbVYy1aJyNoBMQc3IhrJt/28bN5+QTotI9gWg6gtFVf3vy6R2zxvx2HObWLE8RIQawqJRSypQRufl/FR+LT4iJHVDc4mE6xY29Y3Z3d3/wI=", BinaryEncoding.Base64), Compression.Deflate))),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"State", type text}, {"Latitude", type number}, {"Longitude", type number}, {"Average Temperature ", type number}})
in
    #"Changed Type"
    """

    print(get_sources(x))
