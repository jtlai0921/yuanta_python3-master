import json

x = '{"name":"John", "age":30}'
y = json.loads(x)
print(type(y))
print(y)
print(y['age'])

x2 = '[{"name":"John", "age":30},' \
     '{"name":"Mary", "age":20}]'

y2 = json.loads(x2)
print(type(y2))
for item in y2:
    print(item['age'])


jsonstr = json.dumps(y2, indent=2, sort_keys=True)
print(jsonstr)
