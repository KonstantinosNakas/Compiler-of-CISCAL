# Name                           AM    Username
# Ilias Kleftakis                2461  cse32461
# Konstantinos Panagiotis Nakas  2501  cse32501


outfile = None


class EntityItem:
    def __init__(self, itemType, itemName, boolean, offset):
        if (itemType == "parameter"):
            self.itemType = "parameter"
            self.itemName = itemName
            self.isIn = boolean # in or inout
            self.offset = offset
        elif (itemType == "function"):
            self.itemType = "function"
            self.itemName = itemName
            self.isFunction = boolean
            self.startQuad = 0
            self.argumentList = list()
            self.frameLength = 0
        elif (itemType == "variable"):
            self.itemType = "variable"
            self.itemName = itemName
            self.offset = offset
        else:
            print("Invalid EntityItem constructor")

    def __repr__(self): # to print nicely
        result = ""
        if self.itemType == "function" and self.isFunction == False:
            result = "procedure" + " " + self.itemName
        else:
            result = self.itemType + " " + self.itemName

        if self.itemType == "variable":
            result += " off: " + str(self.offset)
        elif self.itemType == "function":
            result += str(self.argumentList) + " start: " + str(self.startQuad) + " len: " + str(self.frameLength)
        elif self.itemType == "parameter":
            if self.isIn == True:
                result += " in off: " + str(self.offset)
            else:
                result += " inout off: " + str(self.offset)
        return result


class ScopeItem:
    def __init__(self):
        self.offset = 12
        self.entityItemsList = list()

    def addEntityItem(self, item):
        self.entityItemsList.append(item)
        if item.itemType != "function":
            self.offset += 4


    def addArgumentToLast(self, isIn):
        lastEntity = self.entityItemsList[len(self.entityItemsList) - 1]
        lastEntity.argumentList.append(ArgumentItem(isIn))


    def __repr__(self): # to print nicely
        return str(self.entityItemsList)


class ArgumentItem:
    def __init__(self, isIn):
        self.isIn = isIn # in or inout

    def __repr__(self): # to print nicely
        if (self.isIn):
            return "in"
        else:
            return "inout"


scope = list()

def newScope():
    global scope
    scope.append(ScopeItem())


def deleteScope():
    global scope
    outfile.write("Before deleting scope:\n")
    for i in range(len(scope) - 1, -1, -1):
        outfile.write("Level " + str(i) + ": " + str(scope[i]) + "\n")
    outfile.write("\n")
    scope.pop()


def newVariableEntity(name):
    global scope
    offset = scope[len(scope) - 1].offset
    scope[len(scope) - 1].addEntityItem(EntityItem("variable", name, False, offset))


def newFunctionEntity(name, isFunction):
    global scope
    scope[len(scope) - 1].addEntityItem(EntityItem("function", name, isFunction, 0))


def newParameterEntity(name, isIn):
    global scope
    offset = scope[len(scope) - 1].offset
    scope[len(scope) - 1].addEntityItem(EntityItem("parameter", name, isIn, offset))


def newArgument(isIn):
    global scope
    # find last function in previous scope (pre-last)
    lastScope = scope[len(scope) - 2]
    lastScope.addArgumentToLast(isIn)


def setLastFunctionStartQuad(startQuad):
    global scope
    if len(scope) == 1: return # main program
    # find last function in previous scope (pre-last)
    lastScope = scope[len(scope) - 2]
    lastEntity = lastScope.entityItemsList[len(lastScope.entityItemsList) - 1]
    lastEntity.startQuad = startQuad


def setLastFunctionFrameLength():
    global scope
    # find last function in previous scope (pre-last)
    lastScope = scope[len(scope) - 2]
    currentScope = scope[len(scope) - 1]
    lastEntity = lastScope.entityItemsList[len(lastScope.entityItemsList) - 1]
    lastEntity.frameLength = currentScope.offset


def findEntity(name):
    global scope
    for i in range(len(scope) - 1, -1, -1):
        for j in range(0, len(scope[i].entityItemsList)):
            if name == scope[i].entityItemsList[j].itemName:
                return (scope[i].entityItemsList[j], i)
    return None, None


def getCurrentScopeNumber():
    global scope
    return len(scope) - 1


def getMainFrameLength():
    global scope
    return scope[0].offset


def existsInCurrentScope(name):
    global scope
    i = len(scope) - 1
    for j in range(0, len(scope[i].entityItemsList)):
        if name == scope[i].entityItemsList[j].itemName:
            return True
    return False


def beginSymbolTableOutput(filename):
    global outfile
    outfile = open(filename, "w")


def endSymbolTableOutput():
    global outfile
    outfile.close()
