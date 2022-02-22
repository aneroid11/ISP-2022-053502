def get_number(prompt: str, minimum: int, maximum: int):
    n = input(prompt)
    while not n.isdigit() or not (minimum <= int(n) <= maximum):
        print("invalid input. please try again")
        n = input(prompt)

    return int(n)


def get_n_and_k():
    n = get_number("enter N (the number of symbols in an n-gram, "
                   "from 1 to 50): ",
                   1, 50)
    k = get_number("enter K (the amount of top n-grams you want to get, "
                   "from 1 to 20): ",
                   1, 20)
    return n, k