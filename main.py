from swiftcompiler import gatherSymbols, gatherClasses, gatherConnections

symbols = gatherSymbols("project_examples/case1/Duck.swift")
classes = gatherClasses(symbols)
connections = gatherConnections(classes)

for name in classes:
    classes[name].describe()

for conn in connections:
    conn.describe()