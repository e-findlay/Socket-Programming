import socket
import sys

if len(sys.argv) > 1:
    serverName = sys.argv[1]
else:
    serverName = ''
if len(sys.argv) > 2:
    serverPort = int(sys.argv[2])
else:
    serverPort = 8080
print(serverName, serverPort)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
message = 'GET_BOARD'
clientSocket.send(message.encode())
response = clientSocket.recv(1024)
print(response)
cmd = input()
print(cmd)
clientSocket.close()
