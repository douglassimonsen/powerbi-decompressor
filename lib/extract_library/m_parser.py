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
    try:
        ret = _s.transform(l.parse(query_definition))
    except (lark.exceptions.UnexpectedCharacters, lark.exceptions.UnexpectedEOF):
        ret = []
    return ret


if __name__ == "__main__":
    x = r"""Calendar(Date(2015,1,1), Date(2015,1,1))
    """

    print(get_sources(x))
