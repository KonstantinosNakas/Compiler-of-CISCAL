# Name                           AM    Username
# Ilias Kleftakis                2461  cse32461
# Konstantinos Panagiotis Nakas  2501  cse32501

# This program tests the lexical analyzer.
# Usage: python3 lexical_test.py <filename>
# Tests for lexical analyzer are inside lexical_test_data directory.

import sys
import lexical

if len(sys.argv) != 2:
    print("Usage: python3 lexical_test.py <filename>")
    exit(1)

lexical.initialize(sys.argv[1])

while (True):
    t = lexical.getNextToken()
    if t == None:
        break
    print(t)

print(lexical.getNextToken()) # should print None
print(lexical.getNextToken()) # should print None
print(lexical.getNextToken()) # should print None
