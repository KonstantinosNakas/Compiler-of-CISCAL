# Name                           AM    Username
# Ilias Kleftakis                2461  cse32461
# Konstantinos Panagiotis Nakas  2501  cse32501

import lexical
import error
import intermediate
import symbolTable
import final

token = ""

def program():
    global token
    if token.tokenType == "program":
        getNextToken()
        if token.tokenType == "identifier":
            programName = "__main"
            symbolTable.newScope()
            getNextToken()
            block(programName)
            symbolTable.setLastFunctionFrameLength()
            intermediate.generateQuad("halt", "_", "_", "_")
            intermediate.generateQuad("end_block", programName, "_", "_")
            final.generateFinalCode()
            symbolTable.deleteScope()
            if token != None:
                error.error("Expected 'End-Of-File' but found '"  + token.token + "'.",
                        token.errorData, len(token.token))
        else:
            error.error("Expected program name.", token.errorData, len(token.token))
    else:
        error.error("Expected 'program' but found '"  + token.token + "'.",
                token.errorData, len(token.token))


def block(blockName = None):
    global token
    if token.tokenType == "{":
        getNextToken()
        declarations()
        subprograms()
        if blockName != None:
            symbolTable.setLastFunctionStartQuad(intermediate.nextQuad())
            intermediate.generateQuad("begin_block", blockName, "_", "_")
        sequence()
        if token.tokenType != "}":
            error.error("Expected '}' but found '" + token.token + "'.",
                    token.errorData, len(token.token))
        getNextToken()
    else:
        error.error("Expected '{' but found '" + token.token + "'.",
                token.errorData, len(token.token))


def declarations():
    global token
    if token.tokenType == "declare":
        getNextToken()
        varlist()
        if token.tokenType != "enddeclare":
            error.error("Expected ',' or 'enddeclare' but found '" + token.token + "'.",
                    token.errorData, len(token.token))
        getNextToken()


def varlist():
    global token
    if token.tokenType == "identifier":
        checkAlreadyDeclaredIdentifier()
        symbolTable.newVariableEntity(token.token)
        getNextToken()
        while token.tokenType == ",":
            getNextToken()
            checkAlreadyDeclaredIdentifier()
            symbolTable.newVariableEntity(token.token)
            if token.tokenType != "identifier":
                error.error("Expected identifier but found '" + token.token + "'.",
                        token.errorData, len(token.token))
            getNextToken()


foundReturn = False
isInsideFunction = False

def subprograms():
    global token
    global foundReturn
    global isInsideFunction
    foundReturn = False
    while token.tokenType == "procedure" or token.tokenType == "function":
        isInsideFunctionPrivate = isInsideFunction
        isInsideFunction = False
        if token.tokenType == "function":
            isInsideFunction = True
        getNextToken()
        funcToken = token
        func(isInsideFunction)
        if foundReturn == False and isInsideFunction == True:
            error.error("No 'return' statement found in function.",
                    funcToken.errorData, len(funcToken.token))
        foundReturn = False
        isInsideFunction = isInsideFunctionPrivate


def func(isFunction):
    global token
    if token.tokenType == "identifier":
        checkAlreadyDeclaredIdentifier()
        funcName = token.token
        symbolTable.newFunctionEntity(token.token, isFunction)
        symbolTable.newScope()
        getNextToken()
        funcbody(funcName)
        final.generateFinalCode()
        symbolTable.deleteScope()
    else:
        error.error("Expected identifier but found '" + token.token + "'.",
                token.errorData, len(token.token))


def funcbody(funcName):
    global token
    formalpars()
    getNextToken()
    block(funcName)
    symbolTable.setLastFunctionFrameLength()
    intermediate.generateQuad("end_block", funcName, "_", "_")


def formalpars():
    global token
    if token.tokenType == "(":
        getNextToken()
        formalparlist()
        if token.tokenType != ")":
            error.error("Expected ')' but found '" + token.token + "'.",
                    token.errorData, len(token.token))
    else:
        error.error("Expected '(' but found '" + token.token + "'.",
                token.errorData, len(token.token))


def formalparlist():
    global token
    formalparitem(True)
    while token.tokenType == ",":
        getNextToken()
        formalparitem(False)


def formalparitem(allowNothing):
    global token
    if token.tokenType == "in" or token.tokenType == "inout":
        isIn = False
        if token.tokenType == "in": isIn = True
        getNextToken()
        symbolTable.newArgument(isIn)
        symbolTable.newParameterEntity(token.token, isIn)
        if token.tokenType != "identifier":
            error.error("Expected identifier but found '" + token.token + "'.",
                    token.errorData, len(token.token))
        getNextToken()
    elif not allowNothing:
        error.error("Expected 'in' or 'inout' but found '" + token.token + "'.",
                token.errorData, len(token.token))


def sequence():
    global token
    statement()
    while token.tokenType ==";":
        getNextToken()
        statement()


def brack_or_stat(): # includes brackets_seq
    global token
    if token.tokenType == "{":
        getNextToken()
        sequence()
        if token.tokenType != "}":
            error.error("Expected '}' but found '" + token.token + "'.",
                    token.errorData, len(token.token))
        getNextToken()
    else:
        statement()
        if token.tokenType != ";":
            error.error("Expected ';' but found '" + token.token + "'.",
                    token.errorData, len(token.token))
        getNextToken()


isInsideDoWhile = False

def statement():
    global token
    global foundReturn
    global isInsideFunction
    global isInsideDoWhile
    global exitList
    if token.tokenType == "identifier":
        checkUndeclaredIdentifier()
        identifier = token.token
        getNextToken()
        assignment_stat(identifier)
    elif token.tokenType == "if":
        getNextToken()
        if_stat()
    elif token.tokenType == "do":
        isInsideDoWhile = True
        getNextToken()
        do_while_stat()
        isInsideDoWhile = False
    elif token.tokenType == "while":
        getNextToken()
        while_stat()
    elif token.tokenType == "select":
        getNextToken()
        select_stat()
    elif token.tokenType == "exit":
        t = intermediate.makeList(intermediate.nextQuad())
        exitList = intermediate.merge(exitList, t)
        intermediate.generateQuad("jump", "_", "_", "_")
        if isInsideDoWhile == False:
            error.error("Found 'exit' outside a do-while loop.",
                    token.errorData, len(token.token))
        getNextToken()
    elif token.tokenType == "return":
        foundReturn = True
        if isInsideFunction == False:
            error.error("'return' statement found outside of function.",
                    token.errorData, len(token.token))
        getNextToken()
        return_stat()
    elif token.tokenType == "print":
        getNextToken()
        print_stat()
    elif token.tokenType == "call":
        getNextToken()
        call_stat()


def assignment_stat(identifier):
    global token
    if token.tokenType == ":=":
        getNextToken()
        result = expression()
        intermediate.generateQuad(":=", result, "_", identifier)
    else:
        error.error("Expected ':=' but found '" + token.token + "'.",
                token.errorData, len(token.token))


def if_stat():
    global token
    if token.tokenType == "(":
        getNextToken()
        (condTrue, condFalse) = condition()
        if token.tokenType == ")":
            intermediate.backPatch(condTrue, intermediate.nextQuad())
            getNextToken()
            brack_or_stat()
            ifList = intermediate.makeList(intermediate.nextQuad())
            intermediate.generateQuad("jump", "_", "_", "_")
            intermediate.backPatch(condFalse, intermediate.nextQuad())
            elsepart()
            intermediate.backPatch(ifList, intermediate.nextQuad())
        else:
            error.error("Expected ')' but found '" + token.token + "'.",
                    token.errorData, len(token.token))
    else:
        error.error("Expected '(' but found '" + token.token + "'.",
                token.errorData, len(token.token))


def elsepart():
    global token
    if token.tokenType == "else":
        getNextToken()
        brack_or_stat()


def while_stat():
    global token
    if token.tokenType == "(":
        conditionQuad = intermediate.nextQuad();
        getNextToken()
        (condTrue, condFalse) = condition()
        if token.tokenType == ")":
            intermediate.backPatch(condTrue, intermediate.nextQuad())
            getNextToken()
            brack_or_stat()
            intermediate.generateQuad("jump", "_", "_", conditionQuad)
            intermediate.backPatch(condFalse, intermediate.nextQuad())
        else:
            error.error("Expected ')' but found '" + token.token + "'.",
                    token.errorData, len(token.token))
    else:
        error.error("Expected '(' but found '" + token.token + "'.",
                token.errorData, len(token.token))


def select_stat():
    global token
    if token.tokenType == "(":
        exitList = intermediate.emptyList()
        getNextToken()
        id1 = token.token
        if token.tokenType != "identifier":
            error.error("Expected identifier but found '" + token.token + "'.",
                    token.errorData, len(token.token))
        checkUndeclaredIdentifier()
        getNextToken()
        if token.tokenType == ")":
            getNextToken()
            nextConstantExpected = "1"
            while token.tokenType == "constant":
                id2 = token.token
                if token.token != nextConstantExpected:
                    error.error("In 'select' expected '" + nextConstantExpected + "' but found '" + token.token + "'.",
                            token.errorData, len(token.token))
                nextConstantExpected = str(int(nextConstantExpected) + 1)
                getNextToken()
                if token.tokenType != ":":
                    error.error("Expected ':' but found '" + token.token + "'.",
                            token.errorData, len(token.token))
                getNextToken()
                t = intermediate.makeList(intermediate.nextQuad())
                intermediate.generateQuad("<>", id1, id2, "_")
                brack_or_stat()
                e = intermediate.makeList(intermediate.nextQuad())
                intermediate.generateQuad("jump", "_", "_", "_")
                exitList = intermediate.merge(exitList, e)
                intermediate.backPatch(t, intermediate.nextQuad())
            if token.tokenType != "default":
                error.error("Expected 'default' but found '" + token.token + "'.",
                        token.errorData, len(token.token))
            getNextToken()
            if token.tokenType != ":":
                error.error("Expected ':' but found '" + token.token + "'.",
                        token.errorData, len(token.token))
            getNextToken()
            brack_or_stat()
            intermediate.backPatch(exitList, intermediate.nextQuad())
        else:
            error.error("Expected ')' but found '" + token.token + "'.",
                    token.errorData, len(token.token))
    else:
        error.error("Expected '(' but found '" + token.token + "'.",
                token.errorData, len(token.token))


exitList = intermediate.emptyList()

def do_while_stat():
    global token
    global exitList
    localExitList = exitList
    exitList = intermediate.emptyList()
    sQuad = intermediate.nextQuad()
    brack_or_stat()
    if token.tokenType == "while":
        getNextToken()
        if token.tokenType == "(":
            getNextToken()
            (condTrue, condFalse) = condition()
            intermediate.backPatch(condFalse, intermediate.nextQuad())
            intermediate.backPatch(condTrue, sQuad)
            if token.tokenType != ")":
                error.error("Expected ')' but found '" + token.token + "'.",
                        token.errorData, len(token.token))
            getNextToken()
            intermediate.backPatch(exitList, intermediate.nextQuad())
            exitList = localExitList
        else:
            error.error("Expected '(' but found '" + token.token + "'.",
                    token.errorData, len(token.token))
    else:
        error.error("Expected 'while' but found '" + token.token + "'.",
                token.errorData, len(token.token))


def return_stat():
    global token
    if token.tokenType == "(":
        getNextToken()
        result = expression()
        intermediate.generateQuad("retv", result, "_", "_")
        if token.tokenType != ")":
            error.error("Expected ')' but found '" + token.token + "'.",
                    token.errorData, len(token.token))
        getNextToken()
    else:
        error.error("Expected '(' but found '" + token.token + "'.",
                token.errorData, len(token.token))


def print_stat():
    global token
    if token.tokenType == "(":
        getNextToken()
        result = expression()
        intermediate.generateQuad("out", result, "_", "_")
        if token.tokenType != ")":
            error.error("Expected ')' but found '" + token.token + "'.",
                    token.errorData, len(token.token))
        getNextToken()
    else:
        error.error("Expected '(' but found '" + token.token + "'.",
                token.errorData, len(token.token))


def call_stat():
    global token
    if token.tokenType == "identifier":
        functionItem, _ = symbolTable.findEntity(token.token)
        if functionItem == None or functionItem.itemType != "function" or functionItem.isFunction == True:
            error.error(token.token + " is not a procedure.",
                    token.errorData, len(token.token))

        procedureName = token.token
        getNextToken()
        actualpars(functionItem)
        intermediate.generateQuad("call", procedureName, "_", "_")
    else:
        error.error("Expected identifier but found '" + token.token + "'.",
                token.errorData, len(token.token))


def actualpars(functionItem):
    global token
    if token.tokenType == "(":
        getNextToken()
        actualparlist(functionItem)
        if token.tokenType != ")":
            error.error("Expected ')' but found '" + token.token + "'.",
                    token.errorData, len(token.token))
        getNextToken()
    else:
        error.error("Expected '(' but found '" + token.token + "'.",
                token.errorData, len(token.token))


def actualparlist(functionItem):
    global token
    argumentId = 0
    finalPars = list()
    finalPars.append(actualparitem(True, functionItem, argumentId))
    while token.tokenType == ",":
        getNextToken()
        argumentId += 1
        if argumentId >= len(functionItem.argumentList):
            error.error("Too many arguments to function.",
                token.errorData, len(token.token))
        finalPars.append(actualparitem(False, functionItem, argumentId))
    if argumentId < len(functionItem.argumentList) - 1:
        error.error("Too few arguments to function.",
                token.errorData, len(token.token))
    for element in finalPars:
        if element != None: # we do it here for nested function calls
            intermediate.generateQuad("par", element[0], element[1], "_")


def actualparitem(allowNothing, functionItem, argumentId):
    global token
    if token.tokenType == "in":
        if functionItem.argumentList[argumentId].isIn == False:
            error.error("Expected 'inout' but found 'in'.",
                    token.errorData, len(token.token))
        getNextToken()
        result = expression()
        return (result, "CV")
    elif token.tokenType == "inout":
        if functionItem.argumentList[argumentId].isIn == True:
            error.error("Expected 'in' but found 'inout'.",
                    token.errorData, len(token.token))
        getNextToken()
        if token.tokenType != "identifier":
            error.error("Expected identifier but found '" + token.token + "'.",
                    token.errorData, len(token.token))
        checkUndeclaredIdentifier()
        thisParam = token.token
        getNextToken()
        return (thisParam, "REF")
    elif not allowNothing:
        error.error("Expected 'in' or 'inout' but found '" + token.token + "'.",
                token.errorData, len(token.token))


def condition():
    global token
    (q1True, q1False) = boolterm()
    thisTrue = q1True
    thisFalse = q1False
    while token.tokenType == "or":
        intermediate.backPatch(thisFalse, intermediate.nextQuad())
        getNextToken()
        (q2True, q2False) = boolterm()
        thisTrue = intermediate.merge(thisTrue, q2True)
        thisFalse = q2False
    return (thisTrue, thisFalse)


def boolterm():
    global token
    (r1True, r1False) = boolfactor()
    thisTrue = r1True
    thisFalse = r1False
    while token.tokenType == "and":
        intermediate.backPatch(thisTrue, intermediate.nextQuad())
        getNextToken()
        (r2True, r2False) = boolfactor()
        thisFalse = intermediate.merge(thisFalse, r2False)
        thisTrue = r2True
    return (thisTrue, thisFalse)


def boolfactor():
    global token
    if token.tokenType == "not":
        getNextToken()
        if token.tokenType == "[":
            getNextToken()
            (thisTrue, thisFalse) = condition()
            if token.tokenType != "]":
                error.error("Expected ']' but found '" + token.token + "'.",
                        token.errorData, len(token.token))
            getNextToken()
        else:
            error.error("Expected '[' but found '" + token.token + "'.",
                    token.errorData, len(token.token))
        return (thisFalse, thisTrue)
    elif token.tokenType == "[":
        getNextToken()
        (thisTrue, thisFalse) = condition()
        if token.tokenType != "]":
            error.error("Expected ']' but found '" + token.token + "'.",
                    token.errorData, len(token.token))
        getNextToken()
        return (thisTrue, thisFalse)
    else:
        e1 = expression()
        relop = relational_oper()
        e2 = expression()
        thisTrue = intermediate.makeList(intermediate.nextQuad())
        intermediate.generateQuad(relop, e1, e2, "_")
        thisFalse = intermediate.makeList(intermediate.nextQuad())
        intermediate.generateQuad("jump", "_", "_", "_")
        return (thisTrue, thisFalse)


def expression():
    global token
    optional_sign()
    t1 = term()
    while token.tokenType == "+" or token.tokenType == "-":
        tokenType = token.token
        getNextToken()
        t2 = term()
        w = intermediate.newTemp()
        intermediate.generateQuad(tokenType, t1, t2, w)
        t1 = w
    return t1 


def term():
    global token
    f1 = factor()
    while token.tokenType in "*/":
        tokenType = token.token
        getNextToken()
        f2 = factor()
        w = intermediate.newTemp()
        intermediate.generateQuad(tokenType, f1, f2, w)
        f1 = w
    return f1


def factor():
    global token
    if token.tokenType == "constant":
        const = token.token
        getNextToken()
        return const
    elif token.tokenType == "(":
        getNextToken()
        result = expression()
        if token.tokenType != ")":
            error.error("Expected ')' but found '" + token.token + "'.",
                    token.errorData, len(token.token))
        getNextToken()
        return result
    elif token.tokenType == "identifier":
        checkUndeclaredIdentifier()
        identifier = token
        getNextToken()
        return idtail(identifier)
    else:
        error.error("Expected condition but found '" + token.token + "'.",
                token.errorData, len(token.token))


def idtail(identifier):
    global token
    if token.tokenType == "(":
        functionItem, _ = symbolTable.findEntity(identifier.token)
        if functionItem == None or functionItem.itemType != "function" or functionItem.isFunction == False:
            error.error(identifier.token + " is not a function.",
                    identifier.errorData, len(identifier.token))
        actualpars(functionItem)
        w = intermediate.newTemp()
        intermediate.generateQuad("par", w, "RET", "_")
        intermediate.generateQuad("call", identifier.token, "_", "_")
        return w
    else:
        return identifier.token


def relational_oper():
    global token
    if token.tokenType not in ["=", "<", "<=", "<>", ">=", ">"]:
        error.error("Expected relational operator but found '" + token.token + "'.",
                token.errorData, len(token.token))
    oper = token.token
    getNextToken()
    return oper


def mul_oper():
    global token
    if token.tokenType not in ["*", "/"]:
        error.error("Expected '*' or '/' but found '" + token.token + "'.",
                token.errorData, len(token.token))
    getNextToken()


def optional_sign():
    global token
    if token.tokenType in ["+", "-"]:
        getNextToken()


def getNextToken():
    global token
    tmp = token
    token = lexical.getNextToken()
    # if token == None:
    #     error.error("Unexpected 'End-Of-File' occurred after token '" +
    #             tmp.token + "'.", tmp.errorData, len(tmp.token))


def checkUndeclaredIdentifier():
    identifier, _  = symbolTable.findEntity(token.token)
    if identifier == None:
        error.error("Identifier '" + token.token + "' is not declared for current scope.",
                token.errorData, len(token.token))


def checkAlreadyDeclaredIdentifier():
    if symbolTable.existsInCurrentScope(token.token):
        error.error("Identifier '" + token.token + "' is already declared for current scope.",
                token.errorData, len(token.token))
