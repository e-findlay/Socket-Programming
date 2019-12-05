import socket
import sys
# from os import path, listdir?
from os import path, listdir
from time import strftime, gmtime
from datetime import datetime
import threading
import json


# set hostname to command line input
if len(sys.argv) > 1:
    hostname = sys.argv[1]
else:
    hostname = ''
# set port number to command line input
if len(sys.argv) > 2:
       serverPort = int(sys.argv[2])
else:
    serverPort = 8080


def getMessages(msg):
    # check message has required parameter
    if not msg[1]:
        reply = {'error': 'missing parameter'}
        return reply
    boardName = msg[1]
    # check specified board is in the board directory
    if boardName not in listdir('board'):
        reply = {'error': 'Specified board does not exist'}
        return reply
    filePath = path.join('board', boardName)
    fileContent = []
    filenames = []
    # get reverse sorted list of filenames in required message board directory
    files = sorted(listdir(filePath))[::-1]
    # filter files list to ensure only files are included
    files = [f for f in files if path.isfile(path.join(filePath, f)) and not f.startswith('.')]
    # select 100 most recent files if more than 100 files
    if len(files) > 100:
        files = files[:100]
    for f in files:
        # open file and append content to array
        with open(path.join(filePath, f)) as file:
            content = file.read()
            fileContent.append(content)
    reply = {'files': files, 'content': fileContent}
    return reply

def postMessage(msg):
    # check message contains required parameter for board name
    if not msg[1]:
        reply = {'error': 'missing parameter'}
        return reply
    boardName = msg[1]
    # check specified board is in the board directory
    if boardName not in listdir('board'):
        reply = {'error': 'Specified board does not exist'}
        return reply
    # check message contains required parameter for title
    if not msg[2]:
        reply = {'error': 'missing parameter'}
        return reply
    messageTitle = msg[2]
    # check message contains required parameter for content
    if not msg[3]:
        reply = {'error': 'missing parameter'}
        return reply
    messageContents = msg[3]
    # convert title to required format
    fileName = strftime('%Y%m%d-%H%M%S-' + messageTitle, gmtime())
    # assign filepath to variable
    messageBoardPath = path.join('board', boardName)
    filePath = path.join(messageBoardPath, fileName)
    # try to write file
    try:
        f = open(filePath, 'w')
        f.write(messageContents)
        f.close()
        reply = {'success': "File Created"}
    except:
        reply = {'error': 'Error Creating File'}
    return reply


def getBoards():
        # search boards directory for message boards
        boards = sorted(listdir('board'))
        reply = {'boards': []}
        # if no message boards defined, print error and quit program
        if len(boards) == 0:
            print('No message boards defined')
            sys.exit()
        for board in boards:
            if not path.isfile(path.join('board', board)):
                reply['boards'].append(board)
        return reply

# create server socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# attempt to bind socket to port
try:
    serverSocket.bind((hostname, serverPort))
    serverSocket.listen(5)
# print error and quit program if port busy
except Exception as e:
    print("Busy port: {}".format(e))
    sys.exit()

def clientThread(connection, address):
    ip = address[0]
    port = address[1]
    logData = f"{ip}:{port}"
    # get current time
    logDate = datetime.now().strftime('%d %B %H:%M:%S %Y')
    # concatenate current time to log data
    logData += '    ' + logDate
    #print(f"Connection made from IP: {ip} and port: {port}")
    while True:
        msg = b''
        # loop to receive long messages from client
        while True:
            part = connection.recv(1024)
            msg += part
            if len(part) < 1024:
                break
        msg = msg.decode('utf-8')
        if not msg:
            break
        else:
            msg = json.loads(msg)
            # check if message is get boards request
            if msg[0] == 'GET_BOARDS':
                logData += '    GET_BOARDS'
                reply = getBoards()
            # check if message is get messages request
            elif msg[0] == 'GET_MESSAGES':
                logData += '    GET_MESSAGES'
                reply = getMessages(msg)
            # check if message is post message request
            elif msg[0] == 'POST_MESSAGE':
                logData += '    POST_MESSAGE'
                reply = postMessage(msg)
            # handle invalid request
            else:
                logData += '    UNKNOWN'
                reply = {'error': 'Invalid message'}
        try:
            # if message contains an error, assign error for handling request
            if 'error' in reply.keys():
                logHandled = '    Error \n'
            else:
                logHandled = '    OK \n'
            reply = json.dumps(reply)
            # return reply to client
            connection.sendall(reply.encode())
        except:
            # if message fails to send to client, assign error handling request
            logHandled = '    Error \n'
        # append request handled message to log data
        logData += logHandled
        # open server.log in append mode if already exists
        if path.exists('server.log'):
            mode = 'a'
        # open server.log in write mode if doesn't exist
        else:
            mode = 'w'
        f = open('server.log', mode)
        # write log data to server .log
        f.write(logData)
        # close file
        f.close()
    # close connection
    connection.close()

# infinite loop to create thread for each new request
while True:
    # return error and quit if no message boards defined
    if len(listdir('board')) == 0:
        print('No message boards defined')
        sys.exit()
    try:
        conn, addr = serverSocket.accept()
        threading._start_new_thread(clientThread, (conn, addr))
    # print busy port error and exit
    except Exception as e:
        print('Error: {}'.format(e))
        break
serverSocket.close()
        

