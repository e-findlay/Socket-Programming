import socket
serverName = ''
serverPort = 8080
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
message = 'GET_BOARDS'
clientSocket.send(message.encode())
response = clientSocket.recv(1024)
print(response.decode())
clientSocket.close()
