# Include Python's Socket Library
from socket import *

# Specify Server Address
serverName = 'localhost'
serverPort = 3002

# Create TCP Socket for Client
clientSocket = socket(AF_INET, SOCK_STREAM)

# Connect to TCP Server Socket
clientSocket.connect((serverName,serverPort))

# Recieve user input from keyboard
dataToSend = input('Whatever client wants to send')

# Send! No need to specify Server Name and Server Port! Why?
clientSocket.send(dataToSend.encode())

# Read reply characters! No need to read address! Why?
dataFromServer = clientSocket.recv(1024)

# Print out the received string
print ('From Server:', dataFromServer.decode())

# Close the socket
clientSocket.close()
