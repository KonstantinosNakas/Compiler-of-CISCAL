program exam {
    declare A, b, g, f enddeclare
    \* A := 1; *\
    function p1(in X, inout Y) {
        declare e, f enddeclare
        function p11(inout X) {
            declare e enddeclare
            e := A;
            X := Y;
            f := b;
            return (e)
        }
        b := X;
        e := p11(inout X);
        e := p1(in X, inout Y);
        X := b;
        return (e)
    }
    if (b > 1 and f < 2 or g + 1 < f + b)
        f := p1(in g);
    else
        f := 1;
}
