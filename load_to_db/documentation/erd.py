import graphviz
import jinja2

tables = [
    {
        "name": "reports",
        "rows": [
            ["id", "serial"],
            ["file_path", "text"],
            ["name", "text"],
        ],
    },
    {
        "name": "pages",
        "rows": [
            ["id", "serial"],
            ["report_id", "int"],
            ["name", "text"],
            ["ordinal", "int"],
            ["filter_id", "int"],
            ["config", "jsonb"],
            ["displayOption", "int"],
            ["width", "float"],
            ["height", "float"],
        ],
    },
    {
        "name": "visuals",
        "rows": [
            ["id", "serial"],
            ["pbi_id", "text"],
            ["page_id", "int"],
            ["visual_type", "text"],
            ["height", "float"],
            ["width", "float"],
            ["x", "float"],
            ["y", "float"],
            ["z", "float"],
        ],
    },
    {
        "name": "datasources",
        "rows": [
            ["id", "serial"],
            ["name", "text"],
            ["pbi_id", "text"],
            ["report_id", "int"],
            ["source_type", "text"],
            ["source_details", "jsonb"],
            ["QueryDefinition", "text"],
        ],
    },
    {
        "name": "tables",
        "rows": [
            ["id", "serial"],
            ["pbi_id", "text"],
            ["datasourceID", "int"],
            ["source_type", "text"],
            ["source_details", "jsonb"],
            ["name", "text"],
        ],
    },
    {
        "name": "measures",
        "rows": [
            ["id", "serial"],
            ["pbi_id", "text"],
            ["TableID", "int"],
            ["name", "text"],
            ["Expression", "text"],
        ],
    },
    {
        "name": "table_columns",
        "rows": [
            ["id", "serial"],
            ["pbi_id", "text"],
            ["table_id", "int"],
            ["name", "text"],
            ["data_type", "text"],
            ["isHidden", "boolean"],
            ["expression", "text"],
        ],
    },
    {
        "name": "dax_dependencies",
        "rows": [
            ["id", "serial"],
            ["child_id", "int"],
            ["child_pbi_id", "text"],
            ["child_type", "text"],
            ["parent_id", "int"],
            ["parent_pbi_id", "text"],
            ["parent_type", "text"],
        ],
    },
]
foreign_keys = [
    ["pages:report_id", "reports:id"],
    ["visuals:page_id", "pages:id"],
    ["tables:datasourceID", "datasources:id"],
    ["measures:TableID", "tables:id"],
    ["table_columns:table_id", "tables:id"],
    [
        "dax_dependencies:child_id-right",
        "dax_dependencies:parent_id-right",
        {"style": "dashed"},
    ],
    ["dax_dependencies:child_id", "visuals:id", {"style": "dashed"}],
    ["dax_dependencies:child_id", "measures:id", {"style": "dashed"}],
    ["dax_dependencies:child_id", "table_columns:id", {"style": "dashed"}],
    ["dax_dependencies:parent_id", "measures:id", {"style": "dashed"}],
    ["dax_dependencies:parent_id", "table_columns:id", {"style": "dashed"}],
]
table = jinja2.Template(
    """<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
        <TR><TD COLSPAN="2">{{name}}</TD></TR>
        {% for row in rows %}
            <TR>
                <TD PORT="{{row[0]}}">{{row[0]}}</TD>
                <TD PORT="{{row[0]}}-right">{{row[1]}}</TD>
            </TR>
        {% endfor %}
</TABLE>
>"""
)


def gen_table(dot, table_def):
    dot.node(table_def["name"], table.render(**table_def))


dot = graphviz.Digraph(
    "structs", node_attr={"shape": "plaintext"}, graph_attr={"splines": "polyline"}
)
for fk in foreign_keys:
    if len(fk) == 2:
        fk.append({})
    dot.edge(*fk[:2], **fk[2])
for definition in tables:
    gen_table(dot, definition)
dot.render("test", format="png")
