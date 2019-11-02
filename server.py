import socket

serverPort = 8080
hostname = ''
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((hostname, serverPort))
serverSocket.listen(1)
print('Server Created')
while True:
    connectionSocket, address = serverSocket.accept()
    message = connectionSocket.recv(1024).decode()
    if message == 'GET_BOARD':
        connectionSocket.send(message.encode())
    elif message == 'POST_MESSAGES':
        pass
    elif message == 'POST_MESSAGE':
        pass
    else:
        connectionSocket.send('Error: Command not recognised'.encode())
    connectionSocket.close()
