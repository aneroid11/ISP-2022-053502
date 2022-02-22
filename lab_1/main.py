import re

DEFAULT_N = 4
DEFAULT_K = 10


def split_into_words(text):
    words = re.split("[.,; \t]", text)
    words = list(filter(None, words))
    return words


def all_words_amount(text):
    return len(split_into_words(text))


def count_every_word(text):
    words = split_into_words(text)
    words_amounts = dict()

    for current_word in words:
        words_amounts[current_word] = words.count(current_word)

    return words_amounts


def valid_sentence(inp_str: str):
    return inp_str and not inp_str.isspace()


def split_into_sentences(text):
    sentences = re.split("[!.?]", text)
    sentences = list(filter(valid_sentence, sentences))
    return sentences


def average_words_in_sentence(text):
    sentences = split_into_sentences(text)

    print("\nALL SENTENCES IN TEXT")
    for curr_sent in sentences:
        print(curr_sent)
    print("END")

    return all_words_amount(text) / len(sentences)


def get_median(numbers_list):
    size = len(numbers_list)

    if size % 2 == 0:
        median = (numbers_list[int(size / 2)] + numbers_list[int(size / 2) - 1]) / 2
    else:
        median = numbers_list[int(size / 2)]

    return median


def median_words_in_sentence(text):
    sentences = split_into_sentences(text)
    words_amounts = list()

    for curr_sentence in sentences:
        words_amounts.append(all_words_amount(curr_sentence))

    words_amounts.sort()

    return get_median(words_amounts)


def get_next_n_gram(text: str, index: int):
    if index > 100:
        return "", 0, False

    return "abc", index + 1, True


def get_n_grams(text: str):
    n_grams = dict()
    curr_n_gram, index, result = get_next_n_gram(text, 0)

    while result:
        if curr_n_gram in n_grams:
            n_grams[curr_n_gram] += 1
        else:
            n_grams[curr_n_gram] = 1

        curr_n_gram, index, result = get_next_n_gram(text, index)

    return n_grams


def get_top_k_n_grams(text: str, n=DEFAULT_N, k=DEFAULT_K):
    return {"Lore", "ipsu", "dolo"}


def pass_by_ref(inp: int):
    inp = 5


def main():
    inp_text = input("enter some text please: ")

    print("\n\ncount every word: \n")
    words = count_every_word(inp_text)

    for w in words:
        print(w + ": " + str(words[w]) + " times")

    print("\naverage words in a sentence: " + str(average_words_in_sentence(inp_text)))

    print("\nmedian words in a sentence: " + str(median_words_in_sentence(inp_text)))

    n = 3
    k = 9
    print("\ntop " + str(k) + " " + str(n) + "-grams: ")
    # print(get_top_k_n_grams(inp_text, n, k))
    print(get_n_grams(inp_text))

    variable = 10
    pass_by_ref(variable)
    print(variable)


if __name__ == "__main__":
    main()
