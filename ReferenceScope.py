class ReferenceScope:
    def __init__(self):
        self.rtype = ""
        self.name = ""
        self.inheritances = []
        self.atributes = []
        self.functions = []
        self.conections = {}
    
    def describe(self):
        attributesNames = ""

        for atr in self.atributes:
            attributesNames += "   {}: {}\n".format(atr.name, atr.inheritances[0])

        print("\n{} {}".format(self.rtype, self.name))
        print("* inheritances: {}".format(self.inheritances))
        print("* attributes: \n{}".format(attributesNames))
        print("* functions: {}\n".format(self.functions))
