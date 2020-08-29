\* Invalid return statement in procedure f *\

program noReturn {
    procedure f(in a) {
        function g(inout b) {
            return (b + 1);
        }

        a := a + 1;
        return (a);
    }

    print(f(in 1))
}
