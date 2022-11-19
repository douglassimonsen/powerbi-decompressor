from frozendict import frozendict
import lark

l = lark.Lark(
    """
start: variable? (other* variable)* other* variable?

other: /.+?/

variable.2: table_var? col_var hier_var?

table_var.2: quote_tab_var | unquote_tab_var 
quote_tab_var.2: "'" /[^\']+/ "'"
unquote_tab_var.2: /[^\w]\w+/

col_var.2: "[" /[^\[\]]+/ "]"

hier_var.2: "." col_var
%import common.WS
"""
)


class Variable(lark.Transformer):
    def other(self, args):
        return lark.Discard

    def quote_tab_var(self, args):
        return args[0].value

    def unquote_tab_var(self, args):
        return args[0].value[1:]

    def table_var(self, args):
        return {"table": args[0]}

    def col_var(self, args):
        return {"column": args[0].value}

    def hier_var(self, args):
        return {"hierarchy": args[0]["column"]}

    def variable(self, args):
        return frozendict({k: v for arg in args for k, v in arg.items()})

    def start(self, args):
        return [
            (x.get("table"), x["column"], x.get("hierarchy"))
            for x in {arg for arg in args if isinstance(arg, frozendict)}
        ]


_v = Variable()


def get_variables(dax_statement):
    dax_statement = dax_statement.replace("\n", " ")
    return _v.transform(l.parse(dax_statement))


if __name__ == "__main__":
    import json
    from pathlib import Path

    with open(Path(__file__).parent / "test.json") as f:
        data = json.load(f)
    for row in set(data):
        print(get_variables(row))
