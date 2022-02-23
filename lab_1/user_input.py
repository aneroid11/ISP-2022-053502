"""Functions to validate user input."""


def get_number(prompt: str, minimum: int, maximum: int) -> int:
    """Get a number from user.

    Show prompt, get a number from user and make sure it is valid (a number
    from minimum to maximum).
    """
    n = input(prompt)
    while not n.isdigit() or not (minimum <= int(n) <= maximum):
        print("invalid input. please try again")
        n = input(prompt)

    return int(n)


def get_n_and_k() -> (int, int):
    """Get N and K from user."""
    n = get_number("enter N (the number of symbols in an n-gram, "
                   "from 1 to 50): ",
                   1, 50)
    k = get_number("enter K (the amount of top n-grams you want to get, "
                   "from 1 to 20): ",
                   1, 20)
    return n, k
