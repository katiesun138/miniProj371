# import socket module
from socket import *
import sys
import os

serverPort = 3000
serverSocket = socket(AF_INET, SOCK_STREAM)  # this creates a socket object
path = '/Users/sunfamily/Desktop/miniProject371/test.html'

# serverSocket.settimeout(0.01)

serverSocket.bind(('', serverPort))  # binds to the port
serverSocket.listen(1)  # waits for 1 client connection
print("the server port is binded to port: ", serverPort)
date = None

while True:
    # Establish the connection
    modification_time = os.path.getmtime(path)
    print("entering true loop")
    connectionSocket, addr = serverSocket.accept()
    try:

        # get filename from connectionSocket and open file
        connectionSocket.settimeout(0.001)
        message = connectionSocket.recv(1024)
        # print("WHATTTTTT STATUS:", message.status_code)

        # print(message, '::', message.split()[0], ':', message.split()[1])
        filename = message.split()[1]
        # print("EEEEEK", filename, "DONEEE")

        # print(filename, '||', filename[1:])
        f = open(filename[1:])
        outputdata = f.read()
        # print(outputdata)

        # Send one HTTP header line into socket
        connectionSocket.send(bytes('\nHTTP/1.1 200 OK\n\n', 'UTF-8'))

        # Send the content of the file to the client
        connectionSocket.send(bytes(outputdata, 'UTF-8'))
        connectionSocket.close()

    except timeout:
        print("408 Request Timeout")
        connectionSocket.send(
            bytes('\nHTTP/1.1 408 Request Timeout\n\n', 'UTF-8'))
        connectionSocket.close()

    except FileNotFoundError:
        # Send response message for file not found
        connectionSocket.send(bytes("HTTP/1.1 404 Not Found\r\n", 'UTF-8'))
        connectionSocket.send(bytes("Content-Type: text/html\r\n", 'UTF-8'))
        connectionSocket.send(bytes("\r\n", 'UTF-8'))
        connectionSocket.send(bytes(
            "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n", 'UTF-8'))
        connectionSocket.close()
    except IOError:
        connectionSocket.send(bytes('\nHTTP/1.1 400 Bad Request\n\n', 'UTF-8'))
        connectionSocket.close()
