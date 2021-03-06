# Name                           AM    Username
# Ilias Kleftakis                2461  cse32461
# Konstantinos Panagiotis Nakas  2501  cse32501

import symbolTable

quads = list()

def nextQuad():
    global quads
    return len(quads)


def generateQuad(op, x, y, z):
    global quads
    quads.append([op, x, y, z])


nextTempId = 0

def newTemp():
    global nextTempId
    tempName = "T_" + str(nextTempId)
    nextTempId += 1
    symbolTable.newVariableEntity(tempName)
    return tempName


def emptyList():
    return list()


def makeList(x):
    return [x]


def merge(list1, list2):
    return list1 + list2


def backPatch(myList, z):
    for element in myList:
        quads[element][3] = z

def outputIntermediateCode(filename):
    global quads
    outfile = open(filename, "w")
    for i in range(len(quads)):
        outfile.write(str(i) + ": " + str(quads[i]) + "\n")
    outfile.close()


def outputEquivalentCCode(filename):
    global quads
    outfile = open(filename, "w")
    outfile.write("#include <stdio.h>\n\nint main(void) {\n")
    outputVariables(outfile)
    for i in range(len(quads)):
        outfile.write("\tL_" + str(i) + ": " + getCommand(quads[i]) + "; // " + str(quads[i]) + "\n")
    outfile.write("}\n")
    outfile.close()


def outputVariables(outfile):
    varlist = list()
    for element in quads:
        if element[0] == "begin_block" or element[0] == "end_block":
            continue
        for i in range(1, 4):
            if not str(element[i]).isdigit() and element[i] != "_" and not element[i] in varlist:
                varlist.append(element[i])
    for element in varlist:
        outfile.write("\tint " + element + ";\n")
    outfile.write("\n")


def getCommand(command):
    if command[0] in ["begin_block", "end_block", "halt",  "retv", "call", "par"]:
        return ""
    elif command[0] == "jump":
        return "goto L_" + str(command[3])
    elif command[0] == ":=":
        return command[3] + " = " + str(command[1])
    elif command[0] == "<>":
        return "if (" + str(command[1]) + " != " + str(command[2]) + ") goto L_" + str(command[3])
    elif command[0] == "=":
        return "if (" + str(command[1]) + " == " + str(command[2]) + ") goto L_" + str(command[3])
    elif command[0] == "out":
        return 'printf("%d\\n", ' + command[1] + ")"
    elif command[0] in ["<", ">", "<=", ">="]:
        return "if (" + str(command[1]) + " " + str(command[0]) + " " + str(command[2]) + ") goto L_" + str(command[3])
    elif command[0] in "+-*/":
        return command[3] + " = " + command[1] + " " + command[0] + " " + command[2]
