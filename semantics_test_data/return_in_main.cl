\* Invalid return statement in main program *\

program noReturn {
    function f(in a) {
        function g(inout b) {
            return (b + 1);
        }

        a := a + 1;
        return (a)
    }

    return (f(in 1))
}
