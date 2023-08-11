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

    data = bytearray()

    current_segment_len = 4  # Header bytes
    current_segment = 0
    current_message = ''

    while True:
      try:
        new_data, client_address = server_socket.recvfrom(READ_BUFFER_SIZE)
        data.extend(new_data)

        # For this simple example, the server only commmunicates
        # with a single client
        prev_client_address = prev_client_address or client_address
        if prev_client_address != client_address:
          print('Unrecognized client')
          break

        while len(data) >= current_segment_len:
          current_segment_data = data[:current_segment_len]
          data = data[current_segment_len:]

          if current_segment == 0:
            current_segment = 1
            current_segment_len = int.from_bytes(current_segment_data, 'big')
          elif current_segment == 1:
            current_message = current_segment_data
            print(f'Received:', current_message.decode('utf-8'), end='')
            current_segment = 2
            current_segment_len = 1
          else:
            print(f', Checksum: ', end='')
            checksum = int.from_bytes(current_segment_data, 'big')
            if get_checksum(current_message) == checksum:
              print('OK')
            else:
              print('ERROR')
            current_message = ''
            current_segment = 0
            current_segment_len = 4

      except TimeoutError:
        break


if __name__ == '__main__':
  main()
