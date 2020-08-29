\* This program declares an already declared function *\

program f1 {
    function f1(in a) {
        return (a + 1);
    }

    function f1(inout b) {
        return (b + 1);
    }

    print(f1(5))
    print(f1(5))
}
