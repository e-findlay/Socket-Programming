import socket
import sys
# get servername from cmd line argument
if len(sys.argv) > 1:
    serverName = sys.argv[1]
else:
    serverName = ''
# get port number from cmd line argument
if len(sys.argv) > 2:
    serverPort = int(sys.argv[2])
else:
    serverPort = 8080
print(serverName, serverPort)



def GET_BOARDS(message):
    # create client socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    message = message.encode()
    clientSocket.send(message)
    response = clientSocket.recv(1024).decode()
    # handle error
    if response == 'No message boards defined':
        print(response)
        clientSocket.close()
    response = response.split('/')
    print(response)
    # print board names to command line
    for i, j in enumerate(response[:-1]):
        print('{}. '.format(i+1),j)
    clientSocket.close()
    return response


def GET_MESSAGES(message):
    # create client socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    msg = message.encode()
    clientSocket.connect((serverName, serverPort))
    clientSocket.send(msg)
    response = clientSocket.recv(1024)
    print(response.decode())
    clientSocket.close()

def POST_MESSAGE(message):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    msg = message.encode()
    clientSocket.send(msg)
    response = clientSocket.recv(1024)
    print(response.decode())
    clientSocket.close()


message = 'GET_BOARDS'
response = GET_BOARDS(message)

    # keep running until user enters QUIT
while True:
    cmd = str(input())
    print(cmd)
    if cmd in range(1, len(response)):
        msg = 'GET_MESSAGES'
        msg += '/' + response[int(cmd)]
        GET_MESSAGES(msg)
            
    if cmd == 'POST':
        msg = 'POST_MESSAGE/'
        boardNumber = input('Which board would you like to post to? \n')
        boardName = response[int(boardNumber) - 1]
        msg += str(boardName)
        msg_title = input('Enter your message title: \n')
        print(msg_title == str)
        msg += '/' + str(msg_title)
        msg_content = input('Enter your message content: \n')
        msg += '/' + str(msg_content)
        POST_MESSAGE(str(msg))

    if cmd == 'QUIT':
        # break infinite loop
        break
print("QUIT successful")

