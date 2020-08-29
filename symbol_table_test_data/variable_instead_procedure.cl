\* This program tries to use a variable in place of a procedure *\

program p {
    declare x enddeclare

    procedure p1() {
        print(1)
    }

    call x()
}
