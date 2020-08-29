\* This program prints all prime numbers in the given range *\

program prime {

    procedure printPrimes(in startNumber, in endNumber) {
        declare i, isPrime enddeclare

        \* calculates the division modulo x % y *\
        function remainder(inout x, in y) {
            declare i, product, modulo enddeclare
            i := 1;
            product := 0;
            while (product <= x) {
                product := y * i;
                i := i + 1;
            };

            modulo := x - (product - y);
            return (modulo);
        }

        while (startNumber <= endNumber) {
            isPrime := 1;
            i := 2;
            do {
                if (startNumber = 2) exit;;
                if (remainder(inout startNumber, in i) = 0) {
                    isPrime := 0;
                    exit;
                };
                i := i + 1;
            } while (i * i <= startNumber);
            if (isPrime = 1) {
                print(startNumber);
            };
            startNumber := startNumber + 1;
        }
    }

    call printPrimes(in 2, in 100);
}
