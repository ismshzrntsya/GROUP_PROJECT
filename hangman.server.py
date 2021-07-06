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

def Main():
    global client_num
    global words

    # Set up the server
    ip = '192.168.56.108'
    if len(sys.argv) < 2:
        print("Enter the number of PORT ")
        sys.exit()
    port = int(sys.argv[1])

    if len(sys.argv) > 2:
        text_file = open(sys.argv[2], "r")
        words = text_file.read().split(', ')

    s = socket.socket(socket .AF_INET, socket.SOCK_STREAM)  # Create TCP Socket
    print('The server is running on the host ' + ip + '| port ' + str(port))

    # Bind and Listen
    try:
        s.bind((ip, port))  # Bind to connection
    except socket.error as e:
        print(str(e))
    s.listen(6)  # Listen to X client

    # End

    # Start accepting Client connections
    while True:
        c, addr = s.accept()
        client_num += 1
        print("A connection " + str(client_num) + " is established from: " + str(addr)) 
        start_new_thread(clientThread, (c,))

def getGame(total_players_requested):
    if total_players_requested == 2:
        for game in games:
            if not game.full:
                game.full = True
                return (game, 2)
    if len(games) < 3:
        word = words[random.randint(0, 14)]
        game = Game(word, total_players_requested)
        games.append(game)
        return (game, 1)
    else:
        return -1

def clientThread(c):  # Threaded for client handler
    global client_num

	# Is it a two player game? expected 2, 0
    twoPlayerSignal = c.recv(1024).decode('utf-8')

    if twoPlayerSignal == '2':
        x = getGame(2)
        if x == -1:
            send(c, 'server is overloaded')
        else:
            game, player = x
            send(c, 'Waiting for other player!')

            while not game.full:
                continue
            send(c, 'The Game has Begun!')
            two_player(c, player, game)

    else:
        x = getGame(1)
        if x == -1:
            send(c, 'server is overloaded')
        else:
            game, player = x
            one_player(c, game)
 
def send(c, msg):
    packet = bytes([len(msg)]) + bytes(msg, 'utf8')
    c.send(packet)

def send_game_control_packet(c, game):
    msgFlag = bytes([0])
    data = bytes(game.gameString + ''.join(game.incorrect_letters), 'utf8')
    gamePacket = msgFlag + bytes([len(game.word)]) + bytes([game.incorrect_guesses]) + data
    c.send(gamePacket)

def two_player(c, player, game):
    global client_num                                                  # SEND_2 >>> Player Number

    while True:
        while game.turn != player:
            continue
        game.lock.acquire()

        status = game.getStatus()
        if status != '':
            send_game_control_packet(c, game)
            send(c, status)
            send(c, "The Game is Over!")
            game.changeTurn()
            game.lock.release()
            break

        send(c, 'Now it's your turn!')

        send_game_control_packet(c, game)

        rcvd = c.recv(1024)
        letter_guessed = bytes([rcvd[1]]).decode('utf-8')

        send(c, game.guess(letter_guessed))

        status = game.getStatus()
        if len(status) > 0:
            send_game_control_packet(c, game)
            send(c, status)
            send(c, "Game Over!")
            game.changeTurn()
            game.lock.release()
            break

        send(c, "Waiting for the other player...")
        game.changeTurn()
        game.lock.release()

    if game in games:
        games.remove(game)
    c.close()
    client_num -= 1


def one_player(c, game):
    global client_num

    while True:
        send_game_control_packet(c, game)

        rcvd = c.recv(1024)
        letter_guessed = bytes([rcvd[1]]).decode('utf-8')

        send(c, game.guess(letter_guessed))

        status = game.getStatus()
        if len(status) > 0:
            send_game_control_packet(c, game)
            send(c, status)
            send(c, "The Game is Over!")
            break
    games.remove(game)
    c.close()
    client_num -= 1



if __name__ == '__main__':
    Main()
