import argparse
import socket
import struct
def create_packet(version, header_length, service_type, payload):

    # Figure out the type of payload for packing
    if service_type == 1:
        payload = int(payload)
        payload_bytes = struct.pack('h', payload) # h -> integer (1 byte)
    elif service_type == 2:
        payload = float(payload) 
        payload_bytes = struct.pack('e', payload) # e -> float (2 bytes)
    elif service_type == 3:
        payload_bytes = payload.encode('utf-8') 
    # Figure out the length of the payload
    pay_len = len(payload_bytes)
    
    try: # Pack the args and the payload length into the header. The payload length will be used to figure out how many bytes are needed to be read later
        header = struct.pack('bbbh', version, header_length, service_type, pay_len)
    except struct.error as e:
        print("Error packing")

    packet = header + payload_bytes # Attach the payload to the end for transmission

    return packet

if __name__ == '__main__':
    # Take the args    
    parser = argparse.ArgumentParser(description="Client for packet creation and sending.")
    parser.add_argument('--version', type=int, required=True, help='Packet version')
    parser.add_argument('--header_length', type=int, required=True, help='Length of the packet header')
    parser.add_argument('--service_type', type=int, required=True, help='Service type of the payload (1 for int, 2 for float, 3 for string)')
    parser.add_argument('--payload', type=str, required=True, help='Payload to be packed into the packet')
    parser.add_argument('--host', type=str, default='10.128.0.3', help='Server host')
    parser.add_argument('--port', type=int, default=8080, help='Server port')

    args = parser.parse_args()
    try:
        # Create and send packet using the create_packet function
        packet = create_packet(args.version, args.header_length, args.service_type, args.payload)


        # Connect to the server
        client_socket = socket.socket()
        client_socket.connect((args.host, args.port))

        # While we are connected to the server, do everything below
        while True:

        # Send the packet
            client_socket.send(packet)
        #TODO: recive the packet 
            size = struct.calcsize('bbbh')  # Calculate the size based on the format string
            received_data = client_socket.recv(size)

            if not received_data:  # Check if the received data is empty
                print("Received an empty packet")

            else:
                response = struct.unpack('bbbh', received_data)# Unpack the received data

                if response == 0:
                    print("Message never made it to Server")
                else: # If we received a packet, then separate out the header components
                    version, header_length, service_type, payload_length = response
                    rec_payload = client_socket.recv(payload_length)
                    if service_type == 1:
                        data = struct.unpack('h', rec_payload)[0]
                    elif service_type == 2:
                        data = struct.unpack('e', rec_payload)[0]
                    elif service_type ==3:
                        data = rec_payload.decode('utf-8')
                    print(f"Payload: {data}") # Process and display the payload


            client_socket.close()
    except socket.error as e: # Error handling for common errors
            if e.errno == 111:
                print("Could not find host listening on ", args.host, " ", args.port)
                exit(1)
            elif e.errno == 32:
                print("Server closed unexpectedly")
            elif e.errno == 104:
                print("Connection closed serverside")