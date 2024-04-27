import socket
import struct

def unpack_packet(conn, header_format):
    #Implement header unpacking based on received bytes
    size = struct.calcsize(header_format) # Define the size from our header format
    header_data = conn.recv(size) # Receive as many bytes as our header format size. This is nice because conn.recv() and struct.calcsize both return bytes
    packet = struct.unpack(header_format, header_data)
    #Create a string from the header fields       
    version, header_length, service_type, payload_len = packet
    # Look at the service_type and payload_length to know the type of the payload and the number of bytes to pass
    payload = conn.recv(payload_len)
    if service_type == 1:
        data = struct.unpack('h', payload)[0] # h -> integer
    elif service_type == 2:
        data = struct.unpack('e', payload)[0] # e -> float of 2 bytes
    elif service_type ==3:
        data = payload.decode('utf-8') # If string, just decode it 
    
    print("Payload: ", data)

    # return the string
    return version, header_length, service_type, payload_len, data

# Define host and port for socket
if __name__ == '__main__': 
    host = '10.128.0.3'
    port = 8080

    # Fixed length header -> Version (1 byte), Header Length (1 byte), Service Type (1 byte), Payload Length (2 bytes)
    header_format = 'bbbh'  # b = int (1 byte), h = integer (2 bytes)

    # Create socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port)) # Bind to host and port
            pass
        except socket.error as e:
            if e.errno == 43:
                print(host, "host and  ", port, " already in use ")
        s.listen() # Listen for connections
        print("Socket listening on,", host, " ", port)
        while True: # Once connected, do everything
            conn, addr = s.accept() # Accept incoming connection
            with conn:
                print(f"Connected by: {addr}")
                while True: #While we are connected, take the connection and unpack packets from client
                    try:
                        payload_string = unpack_packet(conn, header_format) 
                        backHeader = struct.pack('bbbh', payload_string[0], payload_string[1], payload_string[2], payload_string[3]) # Pack the header components from before and process payload
                        if payload_string[2] == 1:
                            payload_b = struct.pack("h", payload_string[4])
                        elif payload_string[2] == 2:
                             payload_b = struct.pack("e", payload_string[4])
                        elif payload_string[2] == 3:
                             payload_b = payload_string[4].encode('utf-8')
                        return_packet = backHeader + payload_b
                        conn.send(return_packet) # Send back to client
                    # Once we don't have anything coming from the current connection, leave the second while loop and wait for a new connection. Server does not exit, just waits for a new connection
                    except:
                        print("Connection closed")
                        break