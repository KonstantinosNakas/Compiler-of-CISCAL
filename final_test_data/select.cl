\*
 * This program uses the select statement to print the numbers
 * in range 1...10.
 *\

program selectCode {
    declare x enddeclare

    procedure printNumber(inout x) {
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

    procedure loopNumbers() {
        while (x <= 10) {
            call printNumber(inout x);
            x := x + 1;
        };
    }

    x := 1;
    call loopNumbers();
}
