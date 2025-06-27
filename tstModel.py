from model.model import Model

mymodel = Model()
mymodel.buildGraph(2010, 2016)
res = mymodel.getGraphDetails()

for r in res:
    print(f"{r[0]} -- {r[1]}")
