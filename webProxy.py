from socket import *
import sys


if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

serverPort = 3002
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))  # binds to the port
serverSocket.listen(1)  # waits for 1 client connection

while 1:

    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    print('Received a connection from:', addr)

    rawMessage = connectionSocket.recv(1024)
    # Extract the filename from the given message
    print(rawMessage.split()[1])
    message = rawMessage.decode()
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)

    try:
        # Check whether the file exist in the cache
        f = open(filetouse[1:], "r") 
        outputdata = f.readlines() 
        fileExist = "true"
        print("File exists")

        # ProxyServer finds a cache hit and generates a response message
        connectionSocket.send(bytes("HTTP/1.0 200 OK\r\n", 'UTF-8'))
        connectionSocket.send(bytes("Content-Type:text/html\r\n", 'UTF-8'))
        connectionSocket.send(bytes(outputdata, 'UTF-8'))
        print('Read from cache') 
    
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false": 
        # Create a socket on the proxyserver
            print("File does not exist")
            print("Creating a socket on the proxy server...")
            proxySocket = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace("www.","",1) 
            print(hostn) 
            try:
                # Connect the socket to port 80
                proxySocket.bind((hostn, 80))
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = proxySocket.makefile('r', 0) 
                fileobj.write("GET "+"http://" + filename + " HTTP/1.0\n\n") 
                # Read the response into buffer
                buffer = fileobj.readlines()

                # Create a new file in the cache for the requested file. 
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmpFile = open("./" + filename,"wb")
                tmpFile.write(buffer)
                connectionSocket.send(bytes('HTTP/1.1 200 OK\r\n', 'UTF-8'))    
                connectionSocket.send(bytes("Content-Type:text/html\r\n", 'UTF-8'))  
                connectionSocket.send(bytes(buffer, 'UTF-8'))
            except:
                connectionSocket.send(bytes("HTTP/1.1 400 Bad Request\r\n", 'UTF-8'))
                connectionSocket.send(bytes("Content-Type: text/html\r\n",'UTF-8'))
                connectionSocket.send(bytes("\r\n", 'UTF-8'))
                connectionSocket.send(bytes("<html><head></head><body><h1>400 Bad Request</h1></body></html>\r\n", 'UTF-8'))
                print("Illegal request") 
        else:
            # HTTP response message for file not found
            connectionSocket.send(bytes("HTTP/1.1 404 Not Found\r\n", 'UTF-8'))
            connectionSocket.send(bytes("Content-Type: text/html\r\n",'UTF-8'))
            connectionSocket.send(bytes("\r\n", 'UTF-8'))
            connectionSocket.send(bytes("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n", 'UTF-8'))
    # Close the client and the server sockets 
    connectionSocket.close() 