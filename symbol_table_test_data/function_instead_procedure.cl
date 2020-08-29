\* This program tries to use a function in place of a procedure *\

program p {
    function f() {
        return (1)
    }

    procedure p() {
        print(1)
    }

    call f()
}
