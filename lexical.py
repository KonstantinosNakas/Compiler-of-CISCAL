# Name                           AM    Username
# Ilias Kleftakis                2461  cse32461
# Konstantinos Panagiotis Nakas  2501  cse32501

import string
import error


text = ""
filename = ""

def initialize(this_filename):
    global text
    global filename

    filename = this_filename
    infile = open(this_filename, 'r')
    text = infile.readlines()
    infile.close()


currentLine = 0
currentColumn = -1
lastCharacterReturned = ""
lastLineReturned = -1
lastColumnReturned = -1
returnLastCharacter = False

def getNextCharacter():
    global currentLine
    global currentColumn
    global lastCharacterReturned
    global returnLastCharacter
    global lastLineReturned
    global lastColumnReturned

    if returnLastCharacter == True:
        returnLastCharacter = False
        return (lastCharacterReturned, lastLineReturned, lastColumnReturned)

    # get the next character's position
    currentColumn += 1
    if currentColumn >= len(text[currentLine]):
        currentLine += 1
        currentColumn = 0
    if currentLine >= len(text):
        return None # reached EOF

    lastCharacterReturned = text[currentLine][currentColumn]
    lastLineReturned = currentLine + 1
    lastColumnReturned = currentColumn + 1
    return (text[currentLine][currentColumn], currentLine + 1,
            currentColumn + 1)


def ungetCharacter():
    global returnLastCharacter
    returnLastCharacter = True


currentToken = ""
validSymbols = string.ascii_letters + string.digits + ":+-*/<>=;,{}()[]\n\\    "
state = 0
lastWasMinusSign = False
reachedEOF = False

def getNextToken():
    global filename
    global currentToken
    global validSymbols
    global state
    global lastWasMinusSign
    global reachedEOF

    while True:
        if reachedEOF == True:
            return None
        next_c = getNextCharacter()
        if next_c == None:
            reachedEOF = True
            if state == 7:
                error.error("Reached End-Of-File and comments do not close.",
                        getErrorData(), 2)
            return None

        c = next_c[0] # the actual character
        if c not in validSymbols and state != 7:
            error.error("Invalid character '" + c + "'.",
                    error.ErrorData(filename, next_c[1], next_c[2]), 1)

        # identifier
        if state == 0 and c.isalpha():
            state = 1
            initalizeToken(next_c)
        elif state == 1 and (c.isalpha() or c.isdigit()):
            currentToken += c
        elif state == 1 and not(c.isalpha() or c.isdigit()):
            state = 0
            ungetCharacter()
            return returnToken(getIdentifierType(currentToken))

        # numeric constant
        elif state == 0 and c.isdigit():
            state = 2
            initalizeToken(next_c)
            continue
        elif state == 2 and c.isdigit():
            currentToken += c
            continue
        elif state == 2 and c.isalpha():
            error.error("Invalid numeric constant. Numeric constants " +
                    "should not contain letters.", getErrorData(),
                    len(currentToken) + 1)
        elif state == 2:
            state = 0
            ungetCharacter()
            if int(currentToken) > 32767 and lastWasMinusSign == False:
                error.error("Number is too big. Biggest allowed " +
                        "is 32767.", getErrorData(), len(currentToken))
            elif int(currentToken) > 32768 and lastWasMinusSign == True:
                error.error("Number is too small. Smallest allowed " +
                        "is -32768.", getErrorData(), len(currentToken))
            return returnToken("constant")

        # various one-character symbols
        elif state == 0 and c in "+-/*,;=()[]{}":
            if c == "-":
                lastWasMinusSign = True
            initalizeToken(next_c)
            return returnToken(c)

        # <= <> <
        elif state == 0 and c == "<":
            state = 3
            initalizeToken(next_c)
        elif state == 3 and c in "=>":
            state = 0
            currentToken += c
            return returnToken(currentToken)
        elif state == 3 and c not in "=>":
            state = 0
            ungetCharacter()
            return returnToken(currentToken)

        # >= >
        elif state == 0 and c == ">":
            state = 4
            initalizeToken(next_c)
        elif state == 4 and c == "=":
            state = 0
            currentToken += c
            return returnToken(currentToken)
        elif state == 4 and c != "=":
            state = 0
            ungetCharacter()
            return returnToken(currentToken)

        # : :=
        elif state == 0 and c == ":":
            state = 5
            initalizeToken(next_c)
        elif state == 5 and c == "=":
            state = 0
            currentToken += c
            return returnToken(currentToken)
        elif state == 5 and c.isspace():
            state = 0
            return returnToken(currentToken)
        elif state == 5:
            error.error("Invalid token '" + currentToken + c +
                    "'. Maybe you mean ': ' or ':=' ?", getErrorData(), 2)

        # \* *\ comments
        elif state == 0 and c == "\\":
            state = 6
            initalizeToken(next_c)
        elif state == 6 and c == "*":
            state = 7
        elif state == 6:
            error.error("Invalid character '\\'. For comments, use '\\*' "
                    "and '*\\'.", getErrorData(), 1)
        elif state == 7 and c == "*":
            state = 8
        elif state == 8 and c == '\\':
            state = 0
        elif state == 8:
            state = 7

        else:
            assert(c.isspace() or state == 7)

        lastWasMinusSign = False


tokenStartLine = 0
tokenStartColumn = 0

def initalizeToken(token):
    global currentToken
    global tokenStartLine
    global tokenStartColumn

    currentToken = token[0]
    tokenStartLine = token[1]
    tokenStartColumn = token[2]


def getErrorData():
    global filename
    global tokenStartLine
    global tokenStartColumn

    return error.ErrorData(filename, tokenStartLine, tokenStartColumn)


class Token:
    token = ""
    tokenType = ""
    errorData = None

    def __init__(self, token, tokenType, errorData):
        self.token = token
        self.tokenType = tokenType
        self.errorData = errorData

    def __repr__(self): # to print nicely
        return "['" + self.token + "' of type '" + self.tokenType + "' " + str(self.errorData) + "]"

def returnToken(dataType):
    global filename
    global currentToken
    global tokenStartLine
    global tokenStartColumn

    return Token(currentToken, dataType,
            error.ErrorData(filename, tokenStartLine, tokenStartColumn))


def getIdentifierType(identifier):
    keywords = ["and", "declare", "do", "else", "enddeclare", "exit",
            "procedure", "function", "print", "call", "if", "in", "inout",
            "not", "select", "program", "or", "return", "while", "default"]

    if identifier in keywords:
        return identifier
    else:
        return "identifier"
