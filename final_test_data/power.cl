\*
 * This program computes and prints x^y, where x and y are positive integers
 * using recursion.
 *\

program powerCalculator {
    function power(in base, in powerRaised) {
        if (powerRaised <> 0) {
            return (base * power(in base, in powerRaised - 1));
        } else {
            return (1);
        };
        print(999); \* unreachable *\
    }

    print(power(in 2, in 5));
}
