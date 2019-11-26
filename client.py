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
    clientSocket.settimeout(10)
    # attempt to connect to server
    try:
        clientSocket.connect((serverName, serverPort))
    # print error and quit program if connection unsuccessful
    except:
        print('Server not available')
        sys.exit()
    message = message.encode()
    # send command to server
    clientSocket.send(message)
    # decode response
    try:
        response = clientSocket.recv(1024).decode()
    except socket.timeout:
        print('Timeout Error')
        clientSocket.close()
        sys.exit()
    # handle error and quit program
    if response == 'No message boards defined':
        print(response)
        clientSocket.close()
        sys.exit()
    # convert response to array of message boards
    response = response.split('/')
    print(response)
    # print board names to command line
    for i, j in enumerate(response):
        print('{}. {}'.format(i+1,j))
    # close connection
    clientSocket.close()
    return response


def GET_MESSAGES(message):
    # create client socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.settimeout(10)
    msg = message.encode()
    # attempt to connect to server
    try:
        clientSocket.connect((serverName, serverPort))
    # print error and quit program if connection unsuccessful
    except:
        print('Server not available')
        sys.exit()
    clientSocket.send(msg)
    try:
        response = clientSocket.recv(1024)
    except socket.timeout as error:
        print('Timeout error')
        clientSocket.close()
        sys.exit()
    response = response.decode()
    # separate response into arrays for message titles and message content
    messages = response.split('//')
    # create array of titles
    messageTitles = messages[0].split('/')
    # create array of contents
    messageContent = messages[1].split('/')
    # print title and contents for each message to command line
    for i in range(len(messageTitles)):
        print(f'{messageTitles[i]}: \n{messageContent[i]}\n')
    # close connection
    clientSocket.close()

def POST_MESSAGE(message):
    # create client socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.settimeout(10)
    # attempt to connect to server
    try:
        clientSocket.connect((serverName, serverPort))
    # print error and quit program if connection unsuccessful
    except:
        print('Server not available')
        sys.exit()
    msg = message.encode()
    clientSocket.send(msg)
    try:
        response = clientSocket.recv(1024)
    except socket.timeout:
        print('Timeout Error')
        clientSocket.close()
        sys.exit()
    print(response.decode())
    # close connection
    clientSocket.close()


message = 'GET_BOARDS'
# send message to server to get list of message board names
response = GET_BOARDS(message)

# keep running until user enters QUIT
while True:
    # wait for used input
    cmd = input()
    print(cmd)
    print(len(response))
    if cmd in str(range(1, len(response)+1)):
        msg = 'GET_MESSAGES'
        print(msg)
        msg += '/' + response[int(cmd)-1]
        GET_MESSAGES(msg)
        
    if cmd == 'POST':
        msg = 'POST_MESSAGE/'
        boardNumber = input('Which board would you like to post to? \n')
        boardName = response[int(boardNumber) - 1]
        msg += str(boardName)
        msgTitle = input('Enter your message title: \n')
        print(msgTitle == str)
        msg += '/' + str(msgTitle)
        msgContent = input('Enter your message content: \n')
        msg += '/' + str(msgContent)
        POST_MESSAGE(str(msg))

    if cmd == 'QUIT':
        # break infinite loop
        break

        
print("QUIT successful")

