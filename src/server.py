import socket

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

READ_BUFFER_SIZE = 1024
CHECKSUM_DIVISOR = 256

HEADER_SIZE_BYTES = 4
DATA_CHECKSUM_SIZE_BYTES = 1

def get_checksum(data):
    return sum(data) % CHECKSUM_DIVISOR

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))

        print(f'Listening at port {SERVER_PORT}')
        server_socket.listen()

        # Only the first connection is accepted
        client_connection, (client_host, client_port) = server_socket.accept()
        print(f'Connected with {client_host} at port {client_port}')

        with client_connection:
            while True:
                header_segment = client_connection.recv(HEADER_SIZE_BYTES)
                if not header_segment:
                    break

                # For this simple example, the header is assumed to be correct.
                # So no check is needed
                header = header_segment[:HEADER_SIZE_BYTES]
                data_len = int.from_bytes(header, 'big')

                data_segment = client_connection.recv(data_len + DATA_CHECKSUM_SIZE_BYTES)
                if not data_segment:
                    break

                data = data_segment[:data_len]
                data_checksum = int.from_bytes(
                    data_segment[data_len:data_len+DATA_CHECKSUM_SIZE_BYTES], 'big')

                print(f'Received {data}', end=' ')
                print('OK') if get_checksum(data) == data_checksum else print('ERROR')

if __name__ == '__main__':
    main()
