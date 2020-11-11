class ReferenceScope:

    def __init__(self):
        self.rtype = ""
        self.name = ""
        self.inheritances = []
        self.atributes = []
        self.functions = []
    
    ## Prints out the class information
    def describe(self):
        attributesNames = ""

        for atr in self.atributes:
            attributesNames += "   {}: {}\n".format(atr.name, atr.inheritances[0])

        print("\n{} {}".format(self.rtype, self.name))
        print("* inheritances: {}".format(self.inheritances))
        print("* attributes: \n{}".format(attributesNames))
        print("* functions: {}\n".format(self.functions))

    ## Returns true if has some reference of otherClass
    def checkExternalReference(self, otherClass):
        for attr in self.atributes:
            if attr.inheritances[0] == otherClass.name:
                return True
        return False

class ReferenceConnection:
    def __init__(self):
        self.caller = ReferenceScope()
        self.called = ReferenceScope()

    def describe(self):
        print("{} calls {}".format(self.caller.name, self.called.name))
