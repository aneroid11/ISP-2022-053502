"""Main module - does some processing of text."""

import text_processing
import user_input


def main():
    """Get some text from the user and show some statistics about it."""
    inp_text = input("enter some text please: ")
    while not inp_text:
        inp_text = input("you did not enter any text. please try again: ")

    choosing_nk = input("do you want to specify N and K yourself "
                        "(default values are 4 and 10)? (y/n): ")
    if choosing_nk == 'y':
        n, k = user_input.get_n_and_k()
    else:
        n = 4
        k = 10

    print("\n\ncount every word: \n")
    words = text_processing.count_every_word(inp_text)

    for w in words:
        print(w + ": " + str(words[w]) + " times")

    print("\naverage words in a sentence: " +
          str(text_processing.average_words_in_sentence(inp_text)))

    print("\nmedian words in a sentence: " +
          str(text_processing.median_words_in_sentence(inp_text)))

    print("\ntop " + str(k) + " " + str(n) + "-grams: ")
    print(text_processing.get_top_k_n_grams(inp_text, n, k))


if __name__ == "__main__":
    main()
