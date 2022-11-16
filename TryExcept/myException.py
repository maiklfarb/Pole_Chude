from random import choice

class WordError(Exception):
    def __init__(self, msg):
        super().__init__(self, msg)

winWord = choice([None])
isStart = choice([True])

word = input('Введите слово: ')



def checkWord(text):
    if isStart == True and winWord == None:
        raise WordError("Игра началась, а слово не было создано.")

    if text == winWord:
        print("Вы победили")
    else:
        print("Вы прогиграли")


try:
    checkWord(word)
except WordError as we:
    print(we)