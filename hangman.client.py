import socket
import sys

def Main():
    if len(sys.argv) < 3:
        print("Enter the number of IP address and PORT ")
        sys.exit()

    ip = str(sys.argv[1])
    port = int(sys.argv[2])
    print('The client is running on the host ' + ip + '| port ' + str(port))

    s = socket.socket()
    s.connect((ip, port))

    print("\n                 HANGMAN GAME PYTHON            ")
    print("\nSingle Player or Two Players? (yes=TwoPlayers/no=SinglePlayer)")
    print(">>", end='')
    msg = input().lower()

    #ask player to input name & send it to server
    name = input("Enter Your Name: ")
    print("\nPlayer: ", name)
    s.send(b'PLAYER ON BOARD: '+ name.encode())

    while 1:
        if msg == 'yes' or msg == 'no':
            break
        msg = input('\nPlease enter either yes (TwoPlayers) or no (SinglePlayer)')


    if msg == 'yes':
        # Signal game start for 2 player
        twoPlayerSignal = '2'.encode('utf-8')
        s.send(twoPlayerSignal)
        playGame(s)

    else:
        # Signal game for single player
        twoPlayerSignal = '0'.encode('utf-8')
        s.send(twoPlayerSignal)

        print("A single-player game began")
        playGame(s)

def recv_helper(socket):
    first_byte_value = int(socket.recv(1)[0])
    if first_byte_value == 0:
        x, y = socket.recv(2)
        return 0, socket.recv(int(x)), socket.recv(int(y))
    else:
        return 1, socket.recv(first_byte_value)

def playGame(s):
    while True:
        pkt = recv_helper(s)
        msgFlag = pkt[0]
        if msgFlag != 0:
            msg = pkt[1].decode('utf8')
            print(msg)
            if msg == 'server is overloaded' or 'The Game is Over!' in msg:
                break
        else:
            gameString = pkt[1].decode('utf8')
            incorrect_guesses = pkt[2].decode('utf8')
            print(" ".join(list(gameString)))
            print("\nYour list of incorrect guesses: " + " ".join(incorrect_guesses) + "\n")
            if "_" not in gameString or len(incorrect_guesses) >= 8:
                continue
            else:
                letter_guessed = ''
                valid = False
                while not valid:
                    letter_guessed = input('Letter to guess: ').lower()
                    if letter_guessed in incorrect_guesses or letter_guessed in gameString:
                        print("\nATTENTION! YOU HAVE GUESS THE LETTER " + letter_guessed.upper() + " BEFORE, PLEASE GUESS ANOTHER LETTER.")
                    elif len(letter_guessed) > 1 or not letter_guessed.isalpha():
                        print("\nERROR! PLEASE GUESS ONE LETTER ONLY")
                    else:
                        print(" ~~ Dup Dap Dup Dap ~~ ")
                        valid = True
                msg = bytes([len(letter_guessed)]) + bytes(letter_guessed, 'utf8')
                s.send(msg)

    s.shutdown(socket.SHUT_RDWR)
    s.close()

if __name__ == '__main__':
    Main()
