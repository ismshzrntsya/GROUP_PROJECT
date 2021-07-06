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

    print("Would you like to play the game with two players? (yes/no)")
    print(">>", end='')
    msg = input().lower()

    while 1:
        if msg == 'yes' or msg == 'no':
            break
        msg = input('Please enter either yes or no')

    if msg == 'yes':
        # Signal game start (2P)
        twoPlayerSignal = '2'.encode('utf-8')
        s.send(twoPlayerSignal)
        playGame(s)

    else:
        # Signal game (1P)
        twoPlayerSignal = '0'.encode('utf-8')
        s.send(twoPlayerSignal)

        print("A single-player game began")
        playGame(s)
