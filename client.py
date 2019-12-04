import socket
import sys
import json

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


# function to allow client to receive long messages from server
def receiveAll(socket):
    data = b''
    while True:
        # append part of message received to data
        part = socket.recv(1024)
        data += part
        # if length of part less than 1024 then transmission has finished
        if len(part) < 1024:
            break
    return data.decode()
        

def getBoards(message):
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
    message = json.dumps(message)
    print(message)
    # send command to server
    clientSocket.send(message.encode())
    # decode response
    try:
        response = receiveAll(clientSocket)
        response = json.loads(response)
        print(response)
    except socket.timeout:
        print('Timeout Error')
        clientSocket.close()
        sys.exit()
    # handle error and quit program
    if 'error' in response.keys():
        print(response['error'])
        clientSocket.close()
        sys.exit()
    # convert response to array of message boards
    print(response)
    # print board names to command line
    boardNumber = []
    for i in range(len(response['boards'])):
        print('{}. {}'.format(i+1,response['boards'][i]))
        boardNumber.append(str(i+1))
    print(boardNumber)
    # close connection
    clientSocket.close()
    return response['boards'], boardNumber


def getMessages(message):
    # create client socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.settimeout(10)
    message = json.dumps(message)
    print(message)
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
        response = receiveAll(clientSocket)
    except socket.timeout as error:
        print('Timeout error')
        clientSocket.close()
        sys.exit()
    # separate response into arrays for message titles and message content
    messages = json.loads(response)
    if 'error' in messages.keys():
        print(messages['error'])
        clientSocket.close()
        return
    # create array of titles
    messageTitles = messages['files']
    # create array of contents
    messageContent = messages['content']
    # print title and contents for each message to command line
    for i in range(len(messageTitles)):
        print(f'{messageTitles[i]}: \n{messageContent[i]}\n')
    # close connection
    clientSocket.close()

def postMessage(message):
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
    message = json.dumps(message)
    print(message)
    msg = message.encode()
    clientSocket.send(msg)
    try:
        response = receiveAll(clientSocket)
    except socket.timeout:
        print('Timeout Error')
        clientSocket.close()
        sys.exit()
    response = json.loads(response)
    if 'error' in response.keys():
        print(response['error'])
        clientSocket.close()
        return
    print(response['success'])
    # close connection
    clientSocket.close()


message = ['GET_BOARDS']
# send message to server to get list of message board names
response, boardNumber = getBoards(message)
print('Enter a board number to get a list of messages for the board')
print('Enter POST to add a message to a board')
print('Enter QUIT to exit the program')

# keep running until user enters QUIT
while True:
    # wait for used input
    cmd = input()
    print(cmd)
    # check if input is for getMessages
    if cmd in boardNumber:
        msg = ['GET_MESSAGES']
        print(msg)
        print(response)
        msg.append(response[int(cmd)-1])
        print(msg)
        getMessages(msg)

    # check if input is for postMessage
    elif cmd == 'POST':
        msg = ['POST_MESSAGE']
        boardNumber = input('Which board would you like to post to? \n')
        boardName = response[int(boardNumber) - 1]
        msg.append(boardName)
        msgTitle = input('Enter your message title: \n')
        print(msgTitle == str)
        msg.append(msgTitle)
        msgContent = input('Enter your message content: \n')
        msg.append(msgContent)
        postMessage(msg)

    # check if input is for quitting client
    elif cmd == 'QUIT':
        # break infinite loop
        break

    # make request to server with invalid input
    else:
        # create client socket
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # set timeout to 10 seconds for error handling
        clientSocket.settimeout(10)
        # try to connect clientSocket
        try:
            clientSocket.connect((serverName, serverPort))
            # print error and quit program if connection unsuccessful
        except:
            print('Server not available')
            sys.exit()
        msg = json.dumps(cmd)
        msg = msg.encode()
        clientSocket.send(msg)
        # 
        try:
            invalidResponse = clientSocket.recv(1024).decode()
        # print timeout error if no response in 10 seconds
        except socket.timeout:
            print('Timeout Error')
            clientSocket.close()
            sys.exit()
        # print error message from server
        invalidResponse = json.loads(invalidResponse)
        if 'error' in invalidResponse.keys():
            print(invalidResponse['error'])
        else:
            print(invalidResponse)
        clientSocket.close()

        
print('QUIT successful')

