class ReferenceScope:

    def __init__(self):
        self.rtype = ""
        self.name = ""
        self.inheritances = []
        self.atributes = []
        self.functions = []
        self.parameters = []
    
    ## Prints out the class information
    def describe(self, prefix=""):
        attributesNames = ""
        separator = ""

        for atr in self.atributes:
            attributesNames += "{}    {}: {}\n".format(prefix, atr.name, atr.inheritances[0])

        print("\n{}{} {}".format(prefix, self.rtype, self.name))
        print("{}* inheritances: {}".format(prefix, self.inheritances))
        if len(attributesNames) > 0:
            separator = "\n"
        print("{}* attributes: {}{}".format(prefix, separator, attributesNames))
        print("{}* functions:".format(prefix))
        for func in self.functions:
            func.describe(prefix + '\t')

        print("{}.".format(prefix))

    ## Returns true if has some reference of otherClass
    def checkExternalReference(self, otherClass):

        # local attributes
        for attr in self.atributes:
            if attr.inheritances[0] == otherClass.name:
                return True

        # function attributes
        for func in self.functions:
            for attr in func.atributes:
                if attr.inheritances[0] == otherClass.name:
                    return True
        
        return False

class ReferenceConnection:
    def __init__(self):
        self.caller = ReferenceScope()
        self.called = ReferenceScope()

    def describe(self):
        print("{} calls {}".format(self.caller.name, self.called.name))
