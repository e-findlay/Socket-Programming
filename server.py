import socket
import sys
# from os import path, listdir?
import os
# delete time before submision?
import time
from time import strftime, gmtime
from datetime import datetime
import threading
import json


print(sys.argv)
# set hostname to command line input
if len(sys.argv) > 1:
    hostname = sys.argv[1]
else:
    hostname = ''
print(hostname)
# set port number to command line input
if len(sys.argv) > 2:
       serverPort = int(sys.argv[2])
else:
    serverPort = 8080
print(serverPort)


def getMessages(msg):
    if not msg[1]:
        reply = {'error': 'missing parameter'}
        return reply
    boardName = msg[1]
    if boardName not in os.listdir('board'):
        reply = {'error': 'Specified board does not exist'}
        return reply
    filePath = os.path.join('board', boardName)
    print(filePath)
    fileContent = []
    filenames = []
    files = sorted(os.listdir(filePath))
    print(files)
    if len(files) > 100:
        files = files[:100]
    for f in files:
        print(f)
        if os.path.isfile(os.path.join(filePath, f)) and not f.startswith('.'):
            filenames.append(f)
            with open(os.path.join(filePath, f)) as file:
                content = file.read()
                fileContent.append(content)
    reply = {'files': filenames, 'content': fileContent}
    print(reply)
    return reply

def postMessage(msg):
    print(msg)
    if not msg[1]:
        reply = {'error': 'missing parameter'}
        return reply
    boardName = msg[1]
    if boardName not in os.listdir('board'):
        reply = {'error': 'Specified board does not exist'}
        return reply
    print(boardName)
    if not msg[2]:
        reply = {'error': 'missing parameter'}
        return reply
    messageTitle = msg[2]
    if not msg[3]:
        reply = {'error': 'missing parameter'}
        return reply
    messageContents = msg[3]
    filename = strftime('%Y%m%d-%H%M%S-' + messageTitle, gmtime())
    print(filename)
    
    boardPath = os.path.dirname('board/' + boardName)
    print(boardPath)
    msgboardPath = os.path.join(boardPath, boardName)
    filePath = os.path.join(msgboardPath, filename)
    print(filePath)
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
        boards = sorted(os.listdir('board'))
        reply = {'boards': []}
        # if no message boards defined, print error and quit program
        if len(boards) == 0:
            print('No message boards defined')
            sys.exit()
        for board in boards:
            if not os.path.isfile(os.path.join('board', board)):
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
    print(f"Connection made from IP: {ip} and port: {port}")
    while True:
        msg = b''
        while True:
            part = connection.recv(1024)
            msg += part
            if len(part) < 1024:
                break
        msg = msg.decode('utf-8')
        print(msg)
        if not msg:
            break
        else:
            msg = json.loads(msg)
            print(msg)
            if msg[0] == 'GET_BOARDS':
                logData += '    GET_BOARDS'
                reply = getBoards()
            elif msg[0] == 'GET_MESSAGES':
                logData += '    GET_MESSAGES'
                reply = getMessages(msg)
            elif msg[0] == 'POST_MESSAGE':
                logData += '    POST_MESSAGE'
                reply = postMessage(msg)
            else:
                logData += '    UNKNOWN'
                print(msg[0])
                reply = {'error': 'Invalid message'}
            print(msg)
        try:
            if 'error' in reply.keys():
                logData += '    Error \n'
            else:
                logData += '    OK \n'
            reply = json.dumps(reply)
            connection.sendall(reply.encode())
        except:
            logData += '    Error \n'
        # open server.log in append mode if already exists
        if os.path.exists('server.log'):
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
    if len(os.listdir('board')) == 0:
        print('No message boards defined')
        sys.exit()
    try:
        conn, addr = serverSocket.accept()
        threading._start_new_thread(clientThread, (conn, addr))
    except Exception as e:
        print("Error: {}".format(e))
        break
serverSocket.close()
        

