from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
import numpy as np
import time

class WordleWindow(QMainWindow):
    def __init__(self):
        super(WordleWindow, self).__init__()
        self.setGeometry(300, 300, 400, 600)
        self.setWindowTitle('PyWord')
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText('Text')
        self.label.move(200, 200)

        self.button = QtWidgets.QPushButton(self)
        self.button.setText('Click me!')
        self.button.clicked.connect(self.get_random_word)

    def get_random_word(self):
        file = open('valid-wordle-words.txt', 'r')
        words = [word.replace('\n', '') for word in file.readlines()]
        file.close()
        random_word = words[np.random.randint(len(words))]
        print(random_word)
        self.label.setText(random_word)
        self.update()
        #return random_word

    def update(self):
        self.label.adjustSize()


def window():
    app = QApplication(sys.argv)
    win = WordleWindow()
    win.show()
    sys.exit(app.exec_())


def analyse_words(words=None):
    if words == None:
        file = open('valid-wordle-words.txt', 'r')
        words = [word.replace('\n', '') for word in file.readlines()]
        file.close()
    letters = {}
    for word in words:
        for l in word:
            letters[l] = letters[l] + 1 if l in letters else 1
    for key in letters.keys():
        print(f'{key}: {letters[key]}')


# -1 - banned letter
# 1-5 - letter on this position
# ? - letter on unknown position
# i. e. constraints = [['a', '?'], ['b', -1]]
def satisfy_constraints(word, constraints):
    for c in constraints:
        #print(word, c)
        if c[1] == -1 and c[0] in word:
            return False
        elif 1 <= c[1] <= 5 and word[c[1] - 1] != c[0]:
            return False
        elif c[1] == '?' and c[0] not in word:
            return False
    return True


def find_best_word(constraints):
    


start = time.time()
analyse_words()
print(f'time: {round(time.time()-start,4)}s')
file = open('valid-wordle-words.txt', 'r')
words = [word.replace('\n', '') for word in file.readlines()]
file.close()
counter = 0
words2 = []
for word in words:
    if satisfy_constraints(word, [['a', 1], ['o', -1]]):
        counter += 1
        print(counter, word)
        words2.append(word)
analyse_words(words2)

# file = open('valid-wordle-words.txt', 'r')
# words = file.readlines()
# file.close()
# random_word = words[np.random.randint(len(words))]
# print(random_word)
# window(random_word)
