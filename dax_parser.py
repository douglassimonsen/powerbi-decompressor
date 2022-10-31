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
    function: /[\w\.]+/ "(" (function | arg) ("," (function | arg))* ")"
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




class Sources(lark.Transformer):
    def __init__(self):
        self.sources = []

    def arg(self, args):
        return args[0].value

    def function(self, args):
        f = {
            'func': args[0].value,
            'args': args[1:]
        }
        return f

    def source_filter(self, args):
        return dict(x.children for x in args[1:])

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
            'var': args[0],
            'expr': args[1],
        }

    def line(self, args):
        if len(args) == 0:
            return None
        args = args[0]
        if isinstance(args, str):  # variable
            args = {'var': args}
        return args

    def start(self, lines):
        lines = [x for x in lines if x is not None]
        for line in lines:
            if line.get('expr', {}).get('func') == 'Excel.Workbook':
                self.sources.append({
                    'type': 'Excel.Workbook',
                    'path': line['expr']['args'][0]['args'][0].strip('"'),
                    'sheet': None
                })
        return self
  

x = l.parse(expression)
sources = Sources().transform(x)
print(sources.sources[0])
exit()

for n in x.iter_subtrees():
    if n.data != 'command':
        continue
    if n.children[0].children[0] == 'Excel.Workbook':
        pass
    print()
    exit()
