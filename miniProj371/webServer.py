#import socket module
from socket import *
import sys

serverPort = 80
serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a server socket

while True:
    #Establish the connection
    #connectionSocket, addr = 
    try:
        #get filename from connectionSocket and open file
        #...

        #Send one HTTP header line into socket
        #...

        #Send the content of the file to the client
        #...

        #connectionSocket.close()
    except IOError:
        #Send response message for file not found
        #Close client socket

serverSocket.close()
sys.exit()