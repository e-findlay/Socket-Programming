import socket
import sys
import os

print(sys.argv)
if len(sys.argv) > 1:
    hostname = sys.argv[1]
else:
    hostname = ''
print(hostname)
if len(sys.argv) > 2:
       serverPort = int(sys.argv[2])
else:
    serverPort = 8080
print(serverPort)
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((hostname, serverPort))
serverSocket.listen(1)
print('Server Created')
while True:
    connectionSocket, address = serverSocket.accept()
    message = connectionSocket.recv(1024).decode()
    if message == 'GET_BOARD':
        message = os.listdir('./board')
        connectionSocket.send(message)
    elif message == 'POST_MESSAGES':
        pass
    elif message == 'POST_MESSAGE':
        pass
    else:
        connectionSocket.send('Error: Command not recognised'.encode())
    connectionSocket.close()
