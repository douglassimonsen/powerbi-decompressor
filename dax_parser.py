import json
import lark
# with open('test.json') as f:
#     data = json.load(f)
# for x in data['Partition']:
#     print(x['QueryDefinition'])
#     print('==' * 10)
# exit()

expression = r'''
let
    Source = List.Generate(() =>
  [Result = try country(1) otherwise null, Page=1],
  each [Result] <> null,
  each [Result = try country([Page] + 1) otherwise null, Page=[Page] + 1],
  each [Result]
),
    #"Converted to Table" = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Expanded Column1" = Table.ExpandTableColumn(#"Converted to Table", "Column1", {"iso2Code", "name", "region", "adminregion", "incomeLevel", "lendingType", "capitalCity", "longitude", "latitude", "Attribute:id"}, {"Column1.iso2Code", "Column1.name", "Column1.region", "Column1.adminregion", "Column1.incomeLevel", "Column1.lendingType", "Column1.capitalCity", "Column1.longitude", "Column1.latitude", "Column1.Attribute:id"}),
    #"Column1 region" = #"Expanded Column1"{11}[Column1.region],
    #"Changed Type" = Table.TransformColumnTypes(#"Column1 region",{{"Element:Text", type text}, {"Attribute:id", type text}, {"Attribute:iso2code", type text}})
in
    #"Changed Type"
'''
expression = r'''
Calendar(Date(2015,1,1), Date(2015,1,1))
'''
expression = r"""
let
    Source = Excel.Workbook(File.Contents("C:\Users\mwham\Desktop\test.xlsx"), null, true),
    Kris_Sheet = Source{[Item="Kris",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Kris_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"a", Int64.Type}, {"b", Int64.Type}})
in
    #"Changed Type"
"""
l = lark.Lark('''
    start: line*
    line: "let" | "in" | statement | variable
    statement: variable "=" command


    command: (function | source_filter) ","?
    function: /[\w\.]+/ "(" (function | arg)* ")"
    arg: /[^\(\)]+/

    source_filter: variable "{[" (sf_var ","?)* "]}[Data]"
    sf_var: no_space_variable "=" "\\"" no_space_variable "\\""

    variable: no_space_variable | space_variable
    no_space_variable: /[\w_]+/
    space_variable: /#"[\w ]+"/
    %import common.WS
    %ignore WS
''')


class ExcelSource:
    def __init__(self, source_path=None, source_tab=None):
        self.source_path = source_path
        self.source_tab = source_tab




class RPN(lark.Transformer):
    def __init__(self):
        source_var = None

    def command(self, args):
        if args[0].children[0] == 'Excel.Workbook':
            source_loc = args[0].children[1].children
            if source_loc[0] == 'File.Contents':
                source_path = source_loc[1].children[0].value
            
            self.source_var = ExcelSource(source_path=source_path)

        else:
            print(args[0])

    def start(self, args):
        return args
  

x = l.parse(expression)
RPN().transform(x)
exit()

for n in x.iter_subtrees():
    if n.data != 'command':
        continue
    if n.children[0].children[0] == 'Excel.Workbook':
        pass
    print()
    exit()
