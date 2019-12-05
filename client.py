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
    # decode message and return
    return data.decode()
        

def getBoards(message):
    # create client socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set 10 second time limit
    clientSocket.settimeout(10)
    # attempt to connect to server
    try:
        clientSocket.connect((serverName, serverPort))
    # print error and quit program if connection unsuccessful
    except:
        print('Server not available')
        sys.exit()
    message = json.dumps(message)
    # send command to server
    clientSocket.send(message.encode())
    # decode response
    try:
        response = receiveAll(clientSocket)
        response = json.loads(response)
    except socket.timeout:
        print('Timeout Error')
        clientSocket.close()
        sys.exit()
    # handle error and quit program
    if 'error' in response.keys():
        print(response['error'])
        clientSocket.close()
        sys.exit()
    # print board names to command line
    boardNumber = []
    for i in range(len(response['boards'])):
        print('{}. {}'.format(i+1,response['boards'][i]))
        boardNumber.append(str(i+1))
    # close connection
    clientSocket.close()
    return response['boards'], boardNumber


def getMessages(message):
    # create client socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set 10 second time limit
    clientSocket.settimeout(10)
    message = json.dumps(message)
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
        getResponse = receiveAll(clientSocket)
    except socket.timeout as error:
        print('Timeout error')
        clientSocket.close()
        sys.exit()
    # separate response into arrays for message titles and message content
    messages = json.loads(getResponse)
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
    # set 10 second time limit
    clientSocket.settimeout(10)
    # attempt to connect to server
    try:
        clientSocket.connect((serverName, serverPort))
    # print error and quit program if connection unsuccessful
    except:
        print('Server not available')
        sys.exit()
    message = json.dumps(message)
    msg = message.encode()
    clientSocket.send(msg)
    try:
        postResponse = receiveAll(clientSocket)
    except socket.timeout:
        print('Timeout Error')
        clientSocket.close()
        sys.exit()
    postResponse = json.loads(postResponse)
    if 'error' in postResponse.keys():
        print(postResponse['error'])
        clientSocket.close()
        return
    print(postResponse['success'])
    # close connection
    clientSocket.close()


message = ['GET_BOARDS']
# send message to server to get list of message board names
nameList, numberList = getBoards(message)
print('Enter a board number to get a list of messages for the board')
print('Enter POST to add a message to a board')
print('Enter QUIT to exit the program')

# keep running until user enters QUIT
while True:
    # wait for used input
    cmd = input()
    # check if input is for getMessages
    if cmd in numberList:
        msg = ['GET_MESSAGES']
        msg.append(nameList[int(cmd)-1])
        getMessages(msg)

    # check if input is for postMessage
    elif cmd == 'POST':
        msg = ['POST_MESSAGE']
        # get number of board from user
        boardNumber = input('Which board would you like to post to? \n')
        boardName = nameList[int(boardNumber) - 1]
        msg.append(boardName)
        # get message title from user
        msgTitle = input('Enter your message title: \n')
        msg.append(msgTitle)
        # get message content from user
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
        # try decoding response
        try:
            invalidResponse = receiveAll(clientSocket)
        # print timeout error if no response in 10 seconds
        except socket.timeout:
            print('Timeout Error')
            clientSocket.close()
            sys.exit()
        # print error message from server
        invalidResponse = json.loads(invalidResponse)
        # print error message if response returns an error
        if 'error' in invalidResponse.keys():
            print(invalidResponse['error'])
        # print response
        else:
            print(invalidResponse)
        # close socket
        clientSocket.close()

        
print('QUIT successful')

