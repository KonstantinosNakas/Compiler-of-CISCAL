\* This program uses an undeclared variable *\

program undeclared {
    declare x enddeclare

    print(x + 1);
    print(y + 1); \* y is undeclared *\
}
