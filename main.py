# Name                           AM    Username
# Ilias Kleftakis                2461  cse32461
# Konstantinos Panagiotis Nakas  2501  cse32501

### Main Program ###

import sys
import os

import lexical
import syntax
import intermediate
import symbolTable
import final

if len(sys.argv) != 2:
    print("Usage: python3 " + sys.argv[0] + " <filename.cl>")
    exit(1)

# Get ready to write the symbol table and the final code to files
filename = os.path.splitext(sys.argv[1])[0] # filename without .cl extension
symbolTable.beginSymbolTableOutput(filename + ".symbolTable")
final.beginFinalCodeOutput(filename + ".asm")

# Compile intermediate code
lexical.initialize(sys.argv[1])
syntax.getNextToken()
syntax.program()

# Write intermediate code to file
intermediate.outputIntermediateCode(filename + ".int")
intermediate.outputEquivalentCCode(filename + ".c")

# Close symbol table and final code files
symbolTable.endSymbolTableOutput()
final.endFinalCodeOutput()
