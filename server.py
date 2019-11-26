import socket
import sys
import os
import time
from time import strftime, gmtime
from datetime import datetime
import threading


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
    msg = msg.split('/')
    boardName = msg[1]
    filePath = 'board/' + boardName
    print(filePath)
    filecontent = ''
    filenames = ''
    files = sorted(os.listdir(filePath))
    print(files)
    if len(files) > 100:
        files = files[:100]
    
    for f in files:
        print(f)
        if os.path.isfile(os.path.join(filePath, f)):
            filenames += f + '/'
            with open(os.path.join(filePath, f)) as file:
                content = file.read()
                filecontent += content + '/'
    reply = filenames + '/' + filecontent
    print(reply)
    return reply

def postMessage(msg):
    msg = msg.split('/')
    print(msg)
    boardName = msg[1]
    print(boardName)
    messageTitle = msg[2]
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
        reply = "File Created"
    except:
        reply = "Error Creating File"
    return reply


def getBoards():
        # search boards directory for message boards
        boards = sorted(os.listdir('./board'))
        reply = ''
        # if no message boards defined, print error and quit program
        if len(boards) == 0:
            print('No message boards defined')
            sys.exit()
        for board in boards:
            if not os.path.isfile(os.path.join('board', board)):
                reply += board + '/'
        return reply[:-1]

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
    logData += '\t' + logDate
    print(f"Connection made from IP: {ip} and port: {port}")
    while True:
        msg = connection.recv(1024).decode()
        print(msg)
        if msg == 'GET_BOARDS':
            logData += '\t' + 'GET_BOARDS'
            reply = getBoards()
        elif msg[:12] == 'GET_MESSAGES':
            logData += '\t' + 'GET_MESSAGES'
            reply = getMessages(msg)
        elif msg[:12] == 'POST_MESSAGE':
            logData += '\t' + 'POST_MESSAGE'
            reply = postMessage(msg)
        else:
            logData += '\t' + 'UNKNOWN'
            print(msg[:12])
            reply = "Invalid message"
        if not msg:
            break
        print(msg)
        try:
            connection.sendall(reply.encode())
            logData += '\t' + 'OK'
        except:
            logData += '\t' + 'Error\n'
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
    try:
        conn, addr = serverSocket.accept()
        threading._start_new_thread(clientThread, (conn, addr))
    except Exception as e:
        print("Error: {}".format(e))
        break
serverSocket.close()
        

