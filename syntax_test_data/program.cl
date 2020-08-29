program testProgram {
    declare var1, var2 enddeclare

    procedure hello(inout var1, in var2) {
        function bye() {
            declare var3, var4 enddeclare
            return (bye(in a))
        }
        var3 := -1234 * (-11 * -4);
        if ([z < a] and b - 2 = 0 or not [1 >= b and 1 <> a] ) {
            do exit; while (1 = 1);
            while (4 + var1 = 5) exit;;
            print(2 * -2 * 4 +4);
            var4 := 11
        } else {
            exit;
            exit
        };
        exit;;;;;;;;;;;;;;;;;; \* This is actually allowed! *\
    }
    call hello(inout var1, in -12 * 2);
    select (a)
    1: print(1);
    2: print(2);
    3: print(3);
    default: exit;
}
