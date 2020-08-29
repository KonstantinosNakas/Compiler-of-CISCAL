# Name                           AM    Username
# Ilias Kleftakis                2461  cse32461
# Konstantinos Panagiotis Nakas  2501  cse32501


import symbolTable
import intermediate


def gnvlcode(v):
    entity, i = symbolTable.findEntity(v)
    writeFinalCode("lw $t0, -4($sp)")
    for j in range(symbolTable.getCurrentScopeNumber() - i):
        writeFinalCode("lw $t0, -4($t0)")
    writeFinalCode("add $t0, $t0, -" + str(entity.offset))


def loadvr(v, r):
    entity, i = symbolTable.findEntity(v)
    if entity == None: # constant value
        writeFinalCode("li $t" + str(r) + ", " + str(v))
        return
    scope_depth = symbolTable.getCurrentScopeNumber() - i
    if i == 0: # global variable
        writeFinalCode("lw $t" + str(r) + ", -" + str(entity.offset) + "($s0)")
    elif scope_depth == 0 and ((entity.itemType == "variable") or (entity.itemType == "parameter" and entity.isIn == True)):
        writeFinalCode("lw $t" + str(r) + ", -" + str(entity.offset) + "($sp)")
    elif entity.itemType == "parameter" and entity.isIn == False and scope_depth == 0:
        writeFinalCode("lw $t0, -" + str(entity.offset) + "($sp)")
        writeFinalCode("lw $t" + str(r) + ", ($t0)")
    elif scope_depth != 0 and (entity.itemType == "variable" or
            (entity.itemType == "parameter" and entity.isIn == True)):
        gnvlcode(v)
        writeFinalCode("lw $t" + str(r) + ", ($t0)")
    elif scope_depth != 0 and (entity.itemType == "variable" or
            (entity.itemType == "parameter" and entity.isIn == False)):
        gnvlcode(v)
        writeFinalCode("lw $t0, ($t0)")
        writeFinalCode("lw $t" + str(r) + ", ($t0)")
    else:
        print("ERROR")



def storerv(r, v):
    entity, i = symbolTable.findEntity(v)
    scope_depth = symbolTable.getCurrentScopeNumber() - i
    if i == 0: # global variable
        writeFinalCode("sw $t" + str(r) + ", -" + str(entity.offset) + "($s0)")
    elif scope_depth == 0 and ((entity.itemType == "variable") or (entity.itemType == "parameter" and entity.isIn == True)):
        writeFinalCode("sw $t" + str(r) + ", -" + str(entity.offset) + "($sp)")
    elif entity.itemType == "parameter" and entity.isIn == False and scope_depth == 0:
        writeFinalCode("lw $t0, -" + str(entity.offset) + "($sp)")
        writeFinalCode("sw $t" + str(r) + ", ($t0)")
    elif scope_depth != 0 and (entity.itemType == "variable" or
            (entity.itemType == "parameter" and entity.isIn == True)):
        gnvlcode(v)
        writeFinalCode("sw $t" + str(r) + ", ($t0)")
    elif scope_depth != 0 and (entity.itemType == "variable" or
            (entity.itemType == "parameter" and entity.isIn == False)):
        gnvlcode(v)
        writeFinalCode("lw $t0, ($t0)")
        writeFinalCode("sw $t" + str(r) + ", ($t0)")
    else:
        print("ERROR")


startQuadIndex = 0
def generateFinalCode():
    global startQuadIndex
    nextParameter = 0
    currentFunction = ""
    for i in range(startQuadIndex, intermediate.nextQuad()):
        writeFinalCode("L" + str(i) + ":")
        current = intermediate.quads[i]
        if (current[0] == "jump"):
            writeFinalCode("j L" + str(current[3]))
        elif current[0] in ["<", ">", "<=", ">=", "=", "<>"]:
            loadvr(current[1], 1)
            loadvr(current[2], 2)
            writeFinalCode(getBranch(current[0]) + ", $t1, $t2, L" + str(current[3]))
        elif current[0] == ":=":
            loadvr(current[1], 1)
            storerv(1, str(current[3]))
        elif current[0] in "+-*/":
            loadvr(current[1], 1)
            loadvr(current[2], 2)
            writeFinalCode(getOperator(current[0]) + " $t1, $t1, $t2")
            storerv(1, str(current[3]))
        elif current[0] == "out":
            writeFinalCode("li $v0, 1")
            loadvr(current[1], 1)
            writeFinalCode("add $a0, $t1, 0")
            writeFinalCode("syscall")
            writeFinalCode("addi $a0, $0, 0xA") # To print a newline
            writeFinalCode("addi $v0, $0, 0xB")
            writeFinalCode("syscall")
        elif current[0] == "retv":
            loadvr(current[1], 1)
            writeFinalCode("lw $t0, -8($sp)")
            writeFinalCode("sw $t1, ($t0)")
            writeFinalCode("lw $ra, ($sp)")
            writeFinalCode("jr $ra")
        elif current[0] == "begin_block":
            currentFunction = current[1]
            if current[1] == "__main":
                writeFinalCode("__main:")
                writeFinalCode("add $sp, $sp, " + str(symbolTable.getMainFrameLength()))
                writeFinalCode("move $s0, $sp")
            else:
                writeFinalCode("sw $ra, ($sp)")
        elif current[0] == "end_block":
            if current[1] != "__main": # main function does not return
                writeFinalCode("lw $ra, ($sp)")
                writeFinalCode("jr $ra")
        elif current[0] == "par":
            if nextParameter == 0:
                writeFinalCode("add $fp, $sp, ?")
            if current[2] == "CV":
                loadvr(current[1], 0)
                writeFinalCode("sw $t0, -" + str(12+4*nextParameter) + "($fp)")
            elif current[2] == "REF":
                writeRefParameter(current[1], nextParameter)
            elif current[2] == "RET":
                entity, _ = symbolTable.findEntity(current[1])
                writeFinalCode("add $t0, $sp, -" + str(entity.offset))
                writeFinalCode("sw $t0, -8($fp)")
            nextParameter += 1
        elif current[0] == "call":
            f, fScope = symbolTable.findEntity(current[1])
            if currentFunction == "__main":
                frameLength = symbolTable.getMainFrameLength()
                cScope = -1
            else:
                c, cScope = symbolTable.findEntity(currentFunction)
                frameLength = c.frameLength
            if fScope == cScope:
                writeFinalCode("lw $t0, -4($sp)")
                writeFinalCode("sw $t0, -4($fp)")
            else:
                writeFinalCode("sw $sp, -4($fp)")
            replaceUnknownLength(f.frameLength)
            writeFinalCode("add $sp, $sp, " + str(f.frameLength))
            writeFinalCode("jal L" + str(f.startQuad))
            writeFinalCode("add $sp, $sp, -" + str(f.frameLength))
            nextParameter = 0
        elif current[0] != "halt":
            print("Unknown command: " + current[0])
    startQuadIndex = intermediate.nextQuad()
    flushFinalCode()


def writeRefParameter(parameter, parameterID):
    entity, i = symbolTable.findEntity(parameter)
    scope_depth = symbolTable.getCurrentScopeNumber() - i
    if scope_depth == 0 and ((entity.itemType == "variable") or (entity.itemType == "parameter" and entity.isIn == True)):
        writeFinalCode("add $t0, $sp, -" + str(entity.offset))
        writeFinalCode("sw $t0, -" + str(12+4*parameterID) + "($fp)")
    elif entity.itemType == "parameter" and entity.isIn == False and scope_depth == 0:
        writeFinalCode("lw $t0, -" + str(entity.offset) + "($sp)")
        writeFinalCode("sw $t0, -" + str(12+4*parameterID) + "($fp)")
    elif scope_depth != 0 and (entity.itemType == "variable" or
            (entity.itemType == "parameter" and entity.isIn == True)):
        gnvlcode(parameter)
        writeFinalCode("sw $t0, -" + str(12+4*parameterID) + "($fp)")
    elif scope_depth != 0 and (entity.itemType == "variable" or
            (entity.itemType == "parameter" and entity.isIn == False)):
        gnvlcode(parameter)
        writeFinalCode("lw $t0, ($t0)")
        writeFinalCode("sw $t0, -" + str(12+4*parameterID) + "($fp)")
    else:
        print("ERROR")



def getOperator(op):
    if op == "+": return "add"
    elif op == "-": return "sub"
    elif op == "*": return "mul"
    else: return "div"


def getBranch(relop):
    if relop == "<": return "blt"
    elif relop == ">": return "bgt"
    elif relop == "<=": return "ble"
    elif relop == ">=": return "bge"
    elif relop == "=": return "beq"
    else: return "bne"


outfile = None
def beginFinalCodeOutput(filename):
    global outfile
    outfile = open(filename, "w")
    writeFinalCode("j __main")


def endFinalCodeOutput():
    global outfile
    outfile.close()


outBuffer = ""
def writeFinalCode(line):
    global outBuffer
    outBuffer += line + "\n"


def replaceUnknownLength(length):
    global outBuffer
    outBuffer = outBuffer.replace("?", str(length))


def flushFinalCode():
    global outfile
    global outBuffer
    outfile.write(outBuffer)
    outBuffer = ""
