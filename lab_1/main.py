# hello world

"""
На вход поступают текстовые данные. Необходимо посчитать и вывести:
- сколько раз повторяется каждое слово в указанном тексте
- среднее количество слов в предложении
- медианное количество слов в предложении
- top-K самых часто повторяющихся буквенных N-грам (K и N имеют значения по-умолчанию 10 и 4, но должна быть возможность
задавать их с клавиатуры).
"""

N = 4
K = 10


def count_every_word(text):
    return {"hello": 2, "hi": 1}


inp_text = input("enter some text please: ")
print("you entered: " + inp_text)
print("count every word: ")
words = count_every_word(inp_text)

for w in words:
    print(w + ": " + str(words[w]) + " times")
