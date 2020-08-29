\* This program contains an invalid select statement *\

program Select1 {
    select (a) \* valid *\
        1: print(1);
        2: print(2);
        3: print(3);
        4: print(4);
        5: print(5);
        default: print(6);
    ;

    select (b)
        2: print(2); \* invalid *\
        default: print(3);
}
