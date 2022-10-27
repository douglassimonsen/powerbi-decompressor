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
    Source = Excel.Workbook(File.Contents("C:\Users\mwham\Desktop\test.xlsx"), null, true),
    Kris_Sheet = Source{[Item="Kris",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Kris_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"a", Int64.Type}, {"b", Int64.Type}})
in
    #"Changed Type"
'''
expression = r'''
let
    Source = Excel.Workbook(File.Contents("C:\Users\mwham\Desktop\test.xlsx"), null, true),
    Kris_Sheet = Source{[Item="Kris",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Kris_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"a", Int64.Type}, {"b", Int64.Type}})
in
    #"Changed Type"
'''
l = lark.Lark('''
    start: line*
    line: "let" | "in" | statement | variable
    statement: variable "=" command


    command: /.+/

    variable: no_space_variable | space_variable
    no_space_variable: /[\w_]+/
    space_variable: /#"[\w ]+"/
    %import common.WS
    %ignore WS
''')

x = l.parse(expression)
for n in x.iter_subtrees():
    if n.data != 'command':
        continue
    print(n.children[0])
    exit()
