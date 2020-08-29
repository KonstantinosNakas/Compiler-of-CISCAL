program nestedFuctionCalls {
    function max(in x, in y) {
        if (x > y) {
            return (x)
        } else {
            return (y)
        }
    }

    print(max(in max(in a, in b), in c));
    print(max(in max(in a, in b), in max(in c, in d)))
}
