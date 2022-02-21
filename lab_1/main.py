"""
На вход поступают текстовые данные. Необходимо посчитать и вывести:
- сколько раз повторяется каждое слово в указанном тексте
- среднее количество слов в предложении
- медианное количество слов в предложении
- top-K самых часто повторяющихся буквенных N-грам (K и N имеют значения по-умолчанию 10 и 4, но должна быть возможность
задавать их с клавиатуры).
"""
import re

N = 4
K = 10


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


def split_into_sentences(text):
    sentences = re.split("[!.?]", text)
    sentences = list(filter(None, sentences))
    return sentences


def average_words_in_sentence(text):
    sentences = split_into_sentences(text)

    return all_words_amount(text) / len(sentences)


def main():
    inp_text = input("enter some text please: ")
    
    print("\ncount every word: ")
    words = count_every_word(inp_text)

    for w in words:
        print(w + ": " + str(words[w]) + " times")

    print("\naverage words in a sentence: " + str(average_words_in_sentence(inp_text)))


if __name__ == "__main__":
    main()
