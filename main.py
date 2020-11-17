from swiftcompiler import gatherSymbols, gatherClasses, gatherConnections, extractCalledRanking, gatherNotDeclared
from os import walk


def readFile(file):
    symbols = gatherSymbols("project_examples/Duck.swift")

    classes = gatherClasses(symbols)
    classes = gatherNotDeclared(classes)
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

def readDir(base_path, files = []):
    for (dirpath, _, filenames) in walk(base_path):
        for fname in filenames:
            path = dirpath.replace("\\","/")
            files.append(path + "/" + fname)

def readFiles(files_path):

    classes = {}

    for path in files_path:
        symbols = gatherSymbols(path)
        newClasses = gatherClasses(symbols)
        for cl in newClasses:
            classes[cl] = newClasses[cl]
    
    classes = gatherNotDeclared(classes)
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


## MAIN 
files = []
readDir("project_examples/generic", files)
readFiles(files)
