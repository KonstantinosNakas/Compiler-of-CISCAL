\* This program declares an already declared procedure *\

program p1 {
    procedure p1(in a) {
        print(a + 1);
    }

    procedure p1(inout b) {
        print(b + 1);
    }

    call p1(5)
}
