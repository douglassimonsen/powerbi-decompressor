import lark
import json


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
        lines = [x for x in lines if x is not None]
        for line in lines:
            if line.get("expr", {}).get("func") == "Excel.Workbook":
                self.sources.append(
                    {
                        "type": "Excel.Workbook",
                        "path": line["expr"]["args"][0]["args"][0].strip('"'),
                        "sheet": None,
                    }
                )
            if line.get("expr", {}).get("type") == "source_filter":
                if len(self.sources) != 0:
                    self.sources[-1]["sheet"] = (
                        line.get("expr", {}).get("args", {}).get("Item")
                    )
        return self.sources


_s = Sources()


def get_sources(query_definition):
    try:
        return _s.transform(l.parse(query_definition))
    except (lark.exceptions.UnexpectedCharacters, lark.exceptions.VisitError):
        return []


if __name__ == "__main__":
    x = r"""let
    Source = Sql.Database(SqlServerInstance, SqlServerDatabase),
    dbo_DimProduct = Source{[Schema="dbo",Item="DimProduct"]}[Data],
    #"Filtered Rows" = Table.SelectRows(dbo_DimProduct, each ([FinishedGoodsFlag] = true)),
    #"Removed Other Columns" = Table.SelectColumns(#"Filtered Rows",{"ProductKey", "ProductAlternateKey", "EnglishProductName", "StandardCost", "Color", "ListPrice", "ModelName", "DimProductSubcategory"}),
    #"Expanded DimProductSubcategory" = Table.ExpandRecordColumn(#"Removed Other Columns", "DimProductSubcategory", {"EnglishProductSubcategoryName", "DimProductCategory"}, {"EnglishProductSubcategoryName", "DimProductCategory"}),
    #"Expanded DimProductCategory" = Table.ExpandRecordColumn(#"Expanded DimProductSubcategory", "DimProductCategory", {"EnglishProductCategoryName"}, {"EnglishProductCategoryName"}),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded DimProductCategory",{{"EnglishProductName", "Product"}, {"StandardCost", "Standard Cost"}, {"ListPrice", "List Price"}, {"ModelName", "Model"}, {"EnglishProductSubcategoryName", "Subcategory"}, {"EnglishProductCategoryName", "Category"}, {"ProductAlternateKey", "SKU"}})
in
    #"Renamed Columns" 
    """
    x = [y.strip() for y in x.splitlines() if y.strip() not in ("let", "in")]
    x = "\n".join(x[:2])
    print(_s.transform(l.parse(x)))
