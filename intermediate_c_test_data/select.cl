\*
 * This program uses the select statement to print the value of x if x is
 * in range 1...10 and 999 otherwise.
 *\

program selectCode {
    declare x enddeclare

    x := 4;

    select (x)
        1: print(1);
        2: print(2);
        3: print(3);
        4: print(4);
        5: print(5);
        6: print(6);
        7: print(7);
        8: print(8);
        9: print(9);
        10: print(10);
        default: print(999);
}
