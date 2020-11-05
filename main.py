from swiftcompiler import gatherSymbols, gatherClasses

symbols = gatherSymbols("project_examples/case1/Duck.swift")

classes = gatherClasses(symbols)

for name in classes:
    classes[name].describe()