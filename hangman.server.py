import socket
from _thread import *
import sys
import random
client_num = 0  # Total number of clients
words = [
    'vaccine', 'corona', 'virus', 'antivaccine', 'safe',
    'car', 'strict', 'addition', 'health', 'astrazeneca',
    'cold', 'sick', 'case', 'depressed', 'real'
]
games = []

class Game:
    word = ""
    gameString = ""
    incorrect_guesses = 0
    incorrect_letters = 0
    turn = 1
    lock = 0
    full = False

    def __init__(self, word, total_players_requested):
        self.incorrect_letters = []
        self.lock = allocate_lock()
        self.word = word
        for i in range(len(word)):
            self.gameString += "_"
        if total_players_requested == 1:
            self.full = True

    def getStatus(self):
        if self.incorrect_guesses >= 6:
            return 'You are doomed! :('
        elif not '_' in self.gameString:
            return 'You are the Winner!'
        else:
            return ''

    def guess(self, letter):
        if letter not in self.word or letter in self.gameString:
            self.incorrect_guesses += 1
            self.incorrect_letters.append(letter)
            return 'Incorrect!'
        else:
            gameString = list(self.gameString)
            for i in range(len(self.word)):
                if self.word[i] == letter:
                    gameString[i] = letter
            self.gameString = ''.join(gameString)
            return 'Correct!'

    def changeTurn(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1
