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


"""def get_next_n_gram(text: str, index: int, n: int):
    length = len(text)

    if index > length - n:
        return "", 0, False

    return text[index:n+index], index + 1, True"""


def get_next_n_gram(text: str, index: int, n: int):
    length = len(text)
    curr_n_gram = ""

    while index < length:
        print("curr_n_gram = " + curr_n_gram)
        print("index = " + str(index))

        if not text[index].isalpha():
            curr_n_gram = ""
        else:
            curr_n_gram += text[index]
        index += 1

        if len(curr_n_gram) == n:
            return curr_n_gram, index - n + 1, True

    return "", 0, False


def get_n_grams(text: str, n: int):
    n_grams = dict()
    curr_n_gram, index, result = get_next_n_gram(text, 0, n)

    while result:
        if curr_n_gram in n_grams:
            n_grams[curr_n_gram] += 1
        else:
            n_grams[curr_n_gram] = 1

        curr_n_gram, index, result = get_next_n_gram(text, index, n)

    return n_grams


def get_top_k_n_grams(text: str, n=DEFAULT_N, k=DEFAULT_K):
    n_grams = get_n_grams(text, n)
    top_k_n_grams = dict()

    key_of_maximum = max(n_grams, key=n_grams.get)
    top_k_n_grams[key_of_maximum] = n_grams[key_of_maximum]
    n_grams.pop(key_of_maximum)

    return top_k_n_grams


def main():
    inp_text = input("enter some text please: ")

    while not inp_text:
        inp_text = input("you did not enter any text. please try again: ")

    print("\n\ncount every word: \n")
    words = count_every_word(inp_text)

    for w in words:
        print(w + ": " + str(words[w]) + " times")

    print("\naverage words in a sentence: " + str(average_words_in_sentence(inp_text)))

    print("\nmedian words in a sentence: " + str(median_words_in_sentence(inp_text)))

    n = 3
    k = 9
    print("\ntop " + str(k) + " " + str(n) + "-grams: ")
    print(get_top_k_n_grams(inp_text, n, k))


if __name__ == "__main__":
    main()
