import socket
import argparse
from common import *

READ_BUFFER_SIZE = 1024


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('server_port', type=int)
  args = parser.parse_args()

  assert 1024 <= args.server_port <= 49151

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(('0.0.0.0', args.server_port))

    print(f'Listening at port {args.server_port}')
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

        data_segment = client_connection.recv(
            data_len + DATA_CHECKSUM_SIZE_BYTES)
        if not data_segment:
          break

        data = data_segment[:data_len]
        data_checksum = int.from_bytes(
            data_segment[data_len:data_len+DATA_CHECKSUM_SIZE_BYTES], 'big')

        print(f'Received: {data}, Checksum: ', end='')
        print('OK') if get_checksum(data) == data_checksum else print('ERROR')


if __name__ == '__main__':
  main()
