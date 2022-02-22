def get_median(numbers_list: list):
    size = len(numbers_list)
    half_size = int(size / 2)

    if size % 2 == 0:
        median = (numbers_list[half_size] + numbers_list[half_size - 1]) / 2
    else:
        median = numbers_list[half_size]

    return median