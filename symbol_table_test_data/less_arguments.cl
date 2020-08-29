\* This program calls a procedure providing less arguments than it should. *\

program less {
    declare x enddeclare

    procedure p(inout a, inout b) {
        print(1);
    }

    call p(inout x);
}
