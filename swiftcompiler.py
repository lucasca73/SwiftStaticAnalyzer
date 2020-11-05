from ReferenceScope import ReferenceScope as Reference
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

        # Removing content from static strings
        fileText = re.sub('\".*\"', '\'\'', fileText)
        fileText = re.sub('\'.*\'', '\'\'', fileText)

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

            if scopeStack[-1] in classes:
                classes[scopeStack[-1]].functions.append(funcName)

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
