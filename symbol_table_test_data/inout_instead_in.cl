\* This program passes an inout type parameter instead of an in. *\

program less {
    declare x enddeclare

    procedure p(in a) {
        print(1);
    }

    call p(inout x);
}
