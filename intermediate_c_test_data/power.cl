\* This program computes and prints x^y, where x and y are positive integers *\

program power {
    declare x, y, count, product enddeclare
    x := 2;
    y := 5;

    product := 1;
    count := 0;

    while (count < y) {
        product := product * x;
        count := count + 1;
    };

    print(product);

}
