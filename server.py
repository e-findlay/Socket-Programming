import socket
import sys
import os
from time import strftime, gmtime
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
    filePath = '/boards/' + boardName
    files = ''
    for f in os.listdir(filePath):
        if os.path.isfile(os.path.join(filePath, f)):
            files += f + '/'
    return files

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
        boards = os.listdir('./board')
        reply = ''
        for board in boards:
            reply = board + '/'
        return reply[:-1]

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    serverSocket.bind((hostname, serverPort))
    serverSocket.listen(5)
except Exception as e:
    print("Could not bind server error: {}", e)

def clientThread(connection, address):
    ip = address[0]
    port = address[1]
    print(f"Connection made from IP: {ip} and port: {port}")
    while True:
        msg = connection.recv(1024).decode()
        print(msg)
        if msg == 'GET_BOARDS':
            reply = getBoards()
        elif msg[:12] == 'GET_MESSAGES':
            reply = getMessages(msg)
        elif msg[:12] == 'POST_MESSAGE':
            reply = postMessage(msg)
        else:
            print(msg[:12])
            reply = "Error"
        if not msg:
            break
        print(msg)
        connection.sendall(reply.encode())
    connection.close()
while True:
    try:
        conn, addr = serverSocket.accept()
        threading._start_new_thread(clientThread, (conn, addr))
    except Exception as e:
        print("Error: {}".format(e))
serverSocket.close()
        

