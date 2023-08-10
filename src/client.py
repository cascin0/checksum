import random
import socket

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

CHECKSUM_DIVISOR = 256

HEADER_SIZE_BYTES = 4
DATA_CHECKSUM_SIZE_BYTES = 1

def get_checksum(data):
    return sum(data) % CHECKSUM_DIVISOR

def create_packet(data):
    packet = bytearray()

    header = len(data).to_bytes(HEADER_SIZE_BYTES) # 32 bits header
    data_checksum = get_checksum(data)

    packet.extend(header)
    packet.extend(data)
    packet.extend(data_checksum.to_bytes(DATA_CHECKSUM_SIZE_BYTES)) # 8 bits checksum

    return packet


def main():
    with socket.socket() as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        data = bytearray(b'Hello from client')
        packet = create_packet(data)

        data_segment_start = HEADER_SIZE_BYTES
        data_segment_end = data_segment_start + len(data)

        for _ in range(20):
            packet_ = packet.copy()

            if random.random() < 0.5:
                random_data_offset = random.randrange(0, len(data)-1)
                packet_[data_segment_start + random_data_offset] = 0

            client_socket.sendall(packet_)

if __name__ == '__main__':
    main()
