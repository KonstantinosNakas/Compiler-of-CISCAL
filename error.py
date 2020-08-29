# Name                           AM    Username
# Ilias Kleftakis                2461  cse32461
# Konstantinos Panagiotis Nakas  2501  cse32501

# This file contains error handling routines.

import sys

class ErrorData:
    filename = ""
    line = 1
    column = 1

    def __init__(self, filename, line, column):
        self.filename = filename
        self.line = line
        self.column = column

    def __repr__(self): # to print nicely
        return "in " + self.filename + ":" + str(self.line) + ":" + str(self.column)


def error(description, errorData, underlineLength):
    print(errorData.filename + ":" + str(errorData.line) + ":" +
            str(errorData.column) + ": ERROR: " + description)
    printLine(errorData)
    printUnderline(errorData, underlineLength)
    print("Please fix the above error and try compiling again. " +
            "Compilation aborted.")
    sys.exit(1)


def printLine(errorData):
    infile = open(errorData.filename, 'r')
    text = infile.readlines()
    print("\t", end = "")
    print(text[errorData.line - 1], end = "")
    infile.close()


def printUnderline(errorData, underlineLength):
    # initial whitespace
    print("\t", end = "")
    for i in range(errorData.column - 1):
        print(" ", end = "")

    # underline characters
    for i in range(underlineLength):
        print("^", end = "")
    print("")
