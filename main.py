from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
import numpy as np

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


def analyse_words():
    file = open('valid-wordle-words.txt', 'r')
    words = [word.replace('\n', '') for word in file.readlines()]
    file.close()
    letters = {}
    for word in words:
        for l in word:
            letters[l] = letters[l] + 1 if l in letters else 1
    for key in letters.keys():
        print(f'{key}: {letters[key]}')

import time
start = time.time()
analyse_words()
print(f'time: {round(time.time()-start,4)}s')
# file = open('valid-wordle-words.txt', 'r')
# words = file.readlines()
# file.close()
# random_word = words[np.random.randint(len(words))]
# print(random_word)
# window(random_word)
