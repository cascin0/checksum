import random
import socket
import argparse
from common import *


NUM_PACKETS_TO_SEND = 2000


def create_packet(data):
  packet = bytearray()

  header = len(data).to_bytes(HEADER_SIZE_BYTES)
  data_checksum = get_checksum(data)

  packet.extend(header)
  packet.extend(data)
  packet.extend(data_checksum.to_bytes(MESSAGE_CHECKSUM_SIZE_BYTES))

  return packet


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('server_host', type=str)
  parser.add_argument('server_port', type=int)
  args = parser.parse_args()

  assert 1024 <= args.server_port <= 49151

  possible_messages = [b'Hello', b'Hello from client', b'Hello world']
  possible_packets = [create_packet(message) for message in possible_messages]

  with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    data_segment_start = HEADER_SIZE_BYTES

    for _ in range(NUM_PACKETS_TO_SEND):
      random_message_index = random.randrange(0, len(possible_messages))
      packet = possible_packets[random_message_index].copy()

      if random.random() < 0.5:
        data_len = len(possible_messages[random_message_index])
        random_data_offset = random.randrange(0, data_len)
        packet[data_segment_start + random_data_offset] = 0

      client_socket.sendto(packet, (args.server_host, args.server_port))

    print('Packets sent')


if __name__ == '__main__':
  main()
