# checksum
This is a simple demo to better understand what a checksum is and how it works in the context of network systems.

# How to run
Start the server with `python3 src/server.py 8080`, where the first argument is the listening port.

Start the client with `python3 src/client.py 127.0.0.1 8080`, where the first argument is the IP address of the server and the second one the listening port.

As soon as you launch the client, it will start sending some packets to the server.
The format of the packets is the following:
- 4 bytes for the length of the message (necessary since they're selected at random)
- A variable number of bytes for the message
- 1 byte for the checksum of the message

A percentage of them will have an (artificially) altered message, and the server should be able to spot the errors thanks to the checksum byte.

The console output of the server should be something like:
```
Received: b'Hello', Checksum: OK
Received: b'Hello world', Checksum: OK
Received: b'Hello from clien\x00', Checksum: ERROR
Received: b'Hello world', Checksum: OK
Received: b'\x00ello', Checksum: ERROR
Received: b'Hello from cli\x00nt', Checksum: ERROR
Received: b'Hello worl\x00', Checksum: ERROR
Received: b'Hello world', Checksum: OK
Received: b'Hello world', Checksum: OK
Received: b'He\x00lo', Checksum: ERROR
Received: b'Hello from client', Checksum: OK
```
