"""Contains functions calculating and showing text statistics."""

import re

import median


def split_into_words(text: str) -> list:
    r"""Split text into words.

    Get some text and split it into words by those symbols: '.,; \t'.
    """
    words = re.split("[.,; \t]", text)
    words = list(filter(None, words))
    return words


def all_words_amount(text: str) -> int:
    """Get the number of words in text."""
    return len(split_into_words(text))


def count_every_word(text: str) -> dict:
    """Get the occurrence frequencies of words in text."""
    words = split_into_words(text)
    words_amounts = dict()

    for current_word in words:
        words_amounts[current_word] = words.count(current_word)

    return words_amounts


def valid_sentence(inp_str: str) -> bool:
    """Check if the sentence is not empty or contains only spaces."""
    return inp_str and not inp_str.isspace()


def split_into_sentences(text: str) -> list:
    """Split text into sentences and return the list of sentences."""
    sentences = re.split("[!.?]", text)
    sentences = list(filter(valid_sentence, sentences))
    return sentences


def average_words_in_sentence(text: str) -> float:
    """Get the average number of words in a sentence in text."""
    sentences = split_into_sentences(text)

    return all_words_amount(text) / len(sentences)


def median_words_in_sentence(text: str) -> float:
    """Get the median number of words in a sentence in text."""
    sentences = split_into_sentences(text)
    words_amounts = list()

    for curr_sentence in sentences:
        words_amounts.append(all_words_amount(curr_sentence))

    words_amounts.sort()

    return median.get_median(words_amounts)


def get_next_n_gram(text: str, index: int, n: int) -> (str, int, bool):
    """Get the next N-gram from text.

    Find and return the next N-gram starting from index. Return:
    - the N-gram
    - index after the N-gram
    - True if found the N-gram, False if not.
    """
    length = len(text)
    curr_n_gram = ""

    while index < length:
        if not text[index].isalpha():
            curr_n_gram = ""
        else:
            curr_n_gram += text[index]
        index += 1

        if len(curr_n_gram) == n:
            return curr_n_gram, index - n + 1, True

    return "", 0, False


def get_n_grams(text: str, n: int) -> dict:
    """Get all N-grams and their frequencies from text."""
    n_grams = dict()
    curr_n_gram, index, result = get_next_n_gram(text, 0, n)

    while result:
        if curr_n_gram in n_grams:
            n_grams[curr_n_gram] += 1
        else:
            n_grams[curr_n_gram] = 1

        curr_n_gram, index, result = get_next_n_gram(text, index, n)

    return n_grams


def get_top_k_n_grams(text: str, n: int, k: int) -> dict:
    """Return the top-K N-grams and their frequencies from text."""
    n_grams = get_n_grams(text, n)
    n_grams_len = len(n_grams)

    if n_grams_len < k:
        k = n_grams_len

    top_k_n_grams = dict()

    for i in range(0, k):
        key_of_maximum = max(n_grams, key=n_grams.get)
        top_k_n_grams[key_of_maximum] = n_grams[key_of_maximum]
        n_grams.pop(key_of_maximum)

    return top_k_n_grams
