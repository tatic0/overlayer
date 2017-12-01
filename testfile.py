from collections import OrderedDict

files=OrderedDict()

a = ['a','b','c','d','f']

for i in a:
    files.update({i: None})

print(files)
