\* This program passes an in type parameter instead of an inout. *\

program less {
    declare x enddeclare

    procedure p(inout a) {
        print(1);
    }

    call p(in x);
}
