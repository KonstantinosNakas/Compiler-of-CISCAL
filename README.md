# Compiler-of-CISCAL

Ciscal is a programming language that invented for the needs of an undergraduated subject.

To test the compiler, open a terminal and type:
python3 main.py <cicsal_program>
This will create 4 files: a file ending in .int that is the intermediate
code, a file ending in .c that is the equivalent C code, a file ending in
.asm that is the final MIPS assembly code and a file ending in .symbolTable,
that is the printout of the symbol table before every scope deletion.

Test programs for the final MIPS assembly code are provided in
final_test_data directory. These programs test all features of the Ciscal
language and are enough to verify the correctness of the compiler.

Test programs for the C equivalent intermediate code are provided in
intermediate_c_test_data directory. These programs test all features of the
Ciscal language and are enough to verify the correctness of the compiler.

***IMPORTANT***: Run with Python 3.x, Python 2.x will not work!!!!!
