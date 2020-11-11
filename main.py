from swiftcompiler import gatherSymbols, gatherClasses, gatherConnections, extractCalledRanking

symbols = gatherSymbols("project_examples/case1/Commented.swift")
print(symbols)
classes = gatherClasses(symbols)
connections = gatherConnections(classes)

ranking = extractCalledRanking(connections)

for name in classes:
    classes[name].describe()

for conn in connections:
    conn.describe()

print("\nCounting external references")
i = 0
for called in ranking:
    i += 1
    print("{} - {}:{}".format(i, called.name, ranking[called]))

# End of program
print("\n")