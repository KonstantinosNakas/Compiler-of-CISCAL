\* No return in function f *\

program noReturn {
    function f(in a) {
        function g(inout b) {
            return (b + 1);
        }

        a := 0;
        a := a + 1;
    }

    print(f(in 1))
}
