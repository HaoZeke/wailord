import pandas as pd
import wailord.io as waio

# data = open("te.data").read()
# sv = waio.sv.SchoolVisitor()
# tree = waio.sv.grammar.parse(data)
# sv.visit(tree)
# df = pd.DataFrame.from_records(sv.output, columns = ['School', 'Grade', 'Student number', 'Name', 'Score'])
# print(df)

# data = open("h2mol.xyz").readlines()
# data.pop(1)
# data = ''.join(map(str, data))
# sx = waio.xyz.xyzVisitor()
# tree = waio.xyz.grammar.parse(data)
# outp = sx.visit(tree)
sx = waio.xyz.xyzIO("h2mol.xyz")
outp = sx.read()
print(outp)
# df = pd.DataFrame.from_records(sv.output, columns = ['School', 'Grade', 'Student number', 'Name', 'Score'])
# print(df)
