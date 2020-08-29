\* This program prints all prime numbers in range 1...100 *\

program prime {
    declare i, j, k, isPrime, product, remainder enddeclare

    i := 2;
    while (i <= 100) {
        isPrime := 1;
        j := 2;
        do {
            if (i = 2) exit;;

            k := 1; \* calculate remainder = i % j *\
            product := 0;
            while (product <= i) {
                product := j * k;
                k := k + 1;
            };
            remainder := i - (product - j);

            if (remainder = 0) {
                isPrime := 0;
                exit;
            };
            j := j + 1;
        } while (j * j <= i);
        if (isPrime = 1) {
            print(i);
        };
        i := i + 1;
    }
}
