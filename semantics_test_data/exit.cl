\* This program contains an exit command outside do...while block *\

program invalidExit {
    do exit; while (a = 1);
    do {
        exit;
        exit;
        exit;
    } while (b <> 1);
    exit; \* invalid *\
}
