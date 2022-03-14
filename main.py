from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
import numpy as np
import time
import re


class WordleWindow(QMainWindow):
    def __init__(self):
        super(WordleWindow, self).__init__()
        self.setGeometry(300, 300, 400, 600)
        self.setWindowTitle('PyWord')
        self.initUI()
        file = open('valid-wordle-words.txt', 'r')
        self.words = [word.replace('\n', '') for word in file.readlines()]
        self.words_all = self.words.copy()
        file.close()
        self.get_random_word()

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
        self.secret = random_word
        self.constraints = ''
        self.guessed = 0
        #return random_word

    def update(self):
        self.label.adjustSize()

    def guess_word(self, word=None):
        if word is None:
            word = input('Guess the word: ')
        new_constraints = ''
        if word == self.secret:
            print("SUCCESS")
        for i in range(5):
            if word[i] == self.secret[i]:
                new_constraints += f'{word[i]}{i+1}'
            elif word[i] in self.secret:
                new_constraints += f'{word[i]}?'
            else:
                new_constraints += f'{word[i]}0'
        self.constraints += new_constraints
        self.words = [w for w in self.words if satisfy_constraints(w, self.constraints)]
        self.guessed += 1
        print(new_constraints)
        for w in self.words:
            print(w)
        print(f'{len(self.words)} words')
        self.print_constraints()

    def print_constraints(self):
        constraints_types = [[], [], []]
        for c in [self.constraints[i:i+2] for i in range(0, len(self.constraints), 2)]:
            if c[1] == '0':
                constraints_types[2].append(c[0])
            elif c[1] == '?':
                constraints_types[1].append(c[0])
            else:
                constraints_types[0].append(f'{c[0]}{c[1]}')
        print(f'Found precisely: {constraints_types[0]}\n'
              f'Found: {constraints_types[1]}\n'
              f'Banned: {constraints_types[2]}')


def window():
    app = QApplication(sys.argv)
    win = WordleWindow()
    #win.show()
    for i in range(5):
        find_best_word(win.words, win.constraints)
        win.guess_word()
    sys.exit(app.exec_())


def analyse_words(words=None):
    if words == None:
        file = open('valid-wordle-words.txt', 'r')
        words = [word.replace('\n', '') for word in file.readlines()]
        file.close()
    letters = {}
    for word in words:
        for l in set(word):
            letters[l] = letters[l] + 1 if l in letters else 1
    # for key in letters.keys():
    #     print(f'{key}: {letters[key]}')
    return letters


# 0 - banned letter
# 1-5 - letter on this position
# ? - letter on unknown position
# i. e. constraints = 'a?b0y5'
def satisfy_constraints(word, constraints):
    constraints = [constraints[i:i+2] for i in range(0, len(constraints), 2)]
    #print(constraints)
    for c in constraints:
        c = [c[0], c[1]]
        #print(word, c[0], c[1])
        if c[1] == '?':
            if c[0] not in word:
                return False
            else:
                continue
        c[1] = int(c[1])
        if c[1] == 0 and c[0] in word:
            return False
        elif 1 <= c[1] <= 5 and word[c[1] - 1] != c[0]:
            return False
    return True


def find_best_word(words, words2, constraints):
    letters = analyse_words(words2)
    best = ['', 0]
    for w in words:
        goodness = 0
        for l in set(w):
            #print(l)
            if l not in constraints:
                goodness += letters[l] if l in letters.keys() else 0
            #else:
                #print(f'---{l}')
        if goodness > best[1]:
            best = [w, goodness]
    print(f'Best word: {best[0]}')
    return best[0]

    
def print_constraints(constraints):
    constraints_types = [[], [], []]
    for c in [constraints[i:i+2] for i in range(0, len(constraints), 2)]:
        if c[1] == '0':
            constraints_types[2].append(c[0])
        elif c[1] == '?':
            constraints_types[1].append(c[0])
        else:
            constraints_types[0].append(f'{c[0]}{c[1]}')
    print(f'Found precisely {len(constraints_types[0])}: {constraints_types[0]}\n'
          f'Found {len(constraints_types[1])}: {constraints_types[1]}\n'
          f'Banned {len(constraints_types[2])}: {constraints_types[2]}\n'
          f'constraints: {constraints}')


def solve_wordle(secret=None, auto=True):
    file = open('valid-wordle-words.txt', 'r')
    words = [word.replace('\n', '') for word in file.readlines()]
    all_words = words.copy()
    file.close()
    constraints = ''
    for i in range(6):
        print_constraints(constraints)
        word = find_best_word(all_words, words, constraints)
        if not auto:
            word = input('Guess the word: ')
        if secret is None:
            new_constraints = input('Constraints: ')
            for j in range(5):
                constraints += word[j]+new_constraints[j]
        else:
            print(f'word {word}, secret {secret}')
            for j in range(5):
                if word[j] == secret[j]:
                    constraints += f'{word[j]}{j + 1}'
                elif word[j] in secret:
                    constraints += f'{word[j]}?'
                else:
                    constraints += f'{word[j]}0'
        words = [w for w in words if satisfy_constraints(w, constraints)]
        if len(words) == 1:
            print(f'Wordle solved in {i+1} moves, the word is:', words[0])
            return word[0]
        #for w in words:
            #print(w)
        print(f'{len(words)} words')
        print(f'possible words: {words}')

# start = time.time()
# analyse_words()
# print(f'time: {round(time.time()-start,4)}s')
# file = open('valid-wordle-words.txt', 'r')
# words = [word.replace('\n', '') for word in file.readlines()]
# file.close()
# counter = 0
# words2 = []
# for word in words:
#     if satisfy_constraints(word, 'a1a5'):
#         counter += 1
#         print(counter, word)
#         words2.append(word)
# analyse_words(words2)

#window()
solve_wordle(auto=False)

# file = open('valid-wordle-words.txt', 'r')
# words = file.readlines()
# file.close()
# random_word = words[np.random.randint(len(words))]
# print(random_word)
# window(random_word)
