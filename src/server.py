import socket
import argparse
from common import *

READ_BUFFER_SIZE = 1024


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('server_port', type=int)
  args = parser.parse_args()

  assert 1024 <= args.server_port <= 49151

  with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind(('0.0.0.0', args.server_port))
    server_socket.settimeout(5)

    print(f'Listening at port {args.server_port}')

    prev_client_address = None

    while True:
      try:
        header_segment, client_address = server_socket.recvfrom(
            HEADER_SIZE_BYTES)

        # For this simple example, the server only commmunicates
        # with a single client
        prev_client_address = prev_client_address or client_address
        if prev_client_address != client_address:
          print('Unrecognized client')
          continue

        header = header_segment[:HEADER_SIZE_BYTES]
        data_len = int.from_bytes(header, 'big')

        data_segment, client_address = server_socket.recvfrom(
            data_len + DATA_CHECKSUM_SIZE_BYTES)

        # For this simple example, the server only commmunicates
        # with a single client
        prev_client_address = prev_client_address or client_address
        if prev_client_address != client_address:
          print('Unrecognized client')
          continue

        data = data_segment[:data_len]
        data_checksum = int.from_bytes(
            data_segment[data_len:data_len+DATA_CHECKSUM_SIZE_BYTES], 'big')

        print(f'Received: {data}, Checksum: ', end='')
        print('OK') if get_checksum(data) == data_checksum else print('ERROR')
      except TimeoutError:
        break


if __name__ == '__main__':
  main()
