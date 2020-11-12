from ReferenceScope import ReferenceScope as Reference
from ReferenceScope import ReferenceConnection as Connection
from swiftkeywords import *
import re

def separateSymbol(symbols, separator):
    newSymbols = []

    for breaks in symbols:
        dots = breaks.split(separator)
        last = 1
        for d in dots:
            if d != '':
                newSymbols.append(d)
            if len(dots) > 1 and last < len(dots):
                last += 1
                newSymbols.append(separator)
    
    return newSymbols

def gatherSymbols(path):
    with open(path) as f:
        fileText = f.read()

        # Adding a \n for removing last line that is commented
        fileText += "\n"

        # Removing content from static strings
        fileText = re.sub('\".*\"', '\'\'', fileText)
        fileText = re.sub('\'.*\'', '\'\'', fileText)

        # Removing simple comments
        fileText = re.sub('/.*\n', '', fileText)

        symbols = []

        spacesSplitted = fileText.split(' ')
        for split in spacesSplitted:
            breaklines = split.split('\n')
            for breaks in breaklines:
                if breaks != '':
                    symbols.append(breaks)

        # separating symbols from words
        for separator in ['.', ':', '(', ')', '{', '}', ',', '[', ']']:
            symbols = separateSymbol(symbols, separator)

        return symbols

    return []


def gatherClasses(symbols):

    # Classes dictionary mapping
    classes = {}
    scopeStack = []

    for num, sym in enumerate(symbols, start=0):

        if sym == "}":
            scopeStack.pop()

        # check Variable
        if sym == LET or sym == VAR:
            varName = symbols[num + 1]
            varType = symbols[num + 3]

            if scopeStack[-1] in classes:
                obj = classes[scopeStack[-1]]
                variable = Reference()
                variable.rType = ATTRIBUTE
                variable.name = varName
                variable.inheritances.append(varType)
                obj.atributes.append(variable)

        # check Function
        if sym == FUNC:
            funcName = symbols[num + 1]
            currentScope = scopeStack[-1]
            if currentScope in classes:
                currentClass = classes[currentScope]

                function = Reference()
                function.rtype = FUNC
                function.name = funcName
                
                ## check parameters
                initParams = -1
                endParams = -1
                paramsCounter = 1
                while initParams == -1:
                    paramsCounter += 1
                    if symbols[num + paramsCounter] == '(':
                        # begin param check
                        initParams = num + paramsCounter
                    
                while endParams == -1:
                    paramsCounter += 1
                    if symbols[num + paramsCounter] == ')':
                        # ending param check
                        endParams = num + paramsCounter
                    elif symbols[num + paramsCounter + 1] == ':':
                        newParam = Reference()
                        newParam.rType = ATTRIBUTE
                        newParam.name = symbols[num + paramsCounter]
                        newParam.inheritances.append(symbols[num + paramsCounter + 2])
                        # adding param
                        function.atributes.append(newParam)

                ## check atributes
                currentClass.functions.append(function)

            scopeStack.append(funcName)

        # Check Class
        if sym == CLASS:
            className = symbols[num + 1]
            classObj = {}

            scopeStack.append(className)

            # Creating class
            if not className in classes:
                someClass = Reference()
                someClass.rtype = CLASS
                someClass.name = className
                classes[className] = someClass
                classObj = someClass
            else:
                classObj = classes[className]

            # Check inhiritance
            if symbols[num + 2] == ':':
                inhiritanceCount = 0
                lastSymbol = symbols[num + 3]
                while lastSymbol != '{':
                    if lastSymbol != ',':
                        classObj.inheritances.append(lastSymbol)
                    inhiritanceCount += 1
                    lastSymbol = symbols[num + 3 + inhiritanceCount]

    return classes

def gatherNotDeclared(classes):

    for cl in classes:
        objClass = classes[cl]

        # check in inheritances
        for inheritance in objClass.inheritances:
            if not inheritance in classes:
                notDeclaredClass = Reference()
                notDeclaredClass.name = inheritance
                notDeclaredClass.rtype = UNKNOWN
                classes[inheritance] = notDeclaredClass
        
        # check in attributes
        for atr in objClass.atributes:
            someType = atr.inheritances[0]

            if not someType in classes:
                notDeclaredClass = Reference()
                notDeclaredClass.name = someType
                notDeclaredClass.rtype = UNKNOWN
                classes[someType] = notDeclaredClass

        # check in functions
        for functions in objClass.functions:
            for atr in functions.atributes:
                someType = atr.inheritances[0]
                if not someType in classes:
                    notDeclaredClass = Reference()
                    notDeclaredClass.name = someType
                    notDeclaredClass.rtype = UNKNOWN
                    classes[someType] = notDeclaredClass

        return classes
        

## Return an array with classes externals calls
def gatherConnections(classes):

    connections = []

    for cl1_key in classes:
        cl1 = classes[cl1_key]

        for cl2_key in classes:
            cl2 = classes[cl2_key]

            # Check if cl1 calls cl2
            if cl1.checkExternalReference(cl2):
                conn = Connection()
                conn.caller = cl1
                conn.called = cl2
                connections.append(conn)

    return connections

## Computes the counting for called classes
def extractCalledRanking(connections):
        ranking = {}

        for conn in connections:
            if conn.called in ranking:
                ranking[conn.called] += 1
            else:
                ranking[conn.called] = 1

        return ranking
