# Client.py
import socket

# List the Host's IP and a valid port for the connection
HOST = "10.128.0.3"
PORT = 8081

#Create the socket object
try:
    client_socket = socket.socket()
except socket.error as e:
    print("Error defining socket object code: ", e.errno)
#Attempt to connect, and if not, throw an error
try:
    client_socket.connect((HOST, PORT))
except socket.error as e:
    if e.errno == 111:
        print("Could not find host listening on ", HOST, " ", PORT)
        exit(1)
#Continuously send messages until the connection is closed
while True:
    # Get user input
    data = input("Enter a message to send to the server (or 'exit'): ")
    # Create a way to close the connection at will
    if data == 'exit':
        print("disconnecting from ", HOST)
        client_socket.close()
        exit(0)
    else:

     # Send the message to the server
        try:
            client_socket.send(data.encode())
        except socket.error as e:
            if e.errno == 32:
                print("Server closed unexpectedly")
                client_socket.close()
                exit(1)
     # Recieve data from the server
        try:
            rec_data = client_socket.recv(200)
        except socket.error as e:
            if e.errno == 104:
                print("Connection closed serverside")
    # Receive and print the server's response
        print(rec_data)