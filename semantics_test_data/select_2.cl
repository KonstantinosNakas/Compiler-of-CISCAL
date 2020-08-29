\* This program contains an invalid select statement *\

program Select2 {
    select (a) \* valid *\
        default: print(1);
    ;

    select (b)
        1: print(1);
        2: print(2);
        5: print(5); \* invalid *\
        default: print(3);
}
