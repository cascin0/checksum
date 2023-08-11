# checksum
This is a simple demo to better understand what a checksum is and how it works in the context of network systems.

# How to run
Start the server with `python3 src/server.py 8080`, where the first argument is the listening port.

Start the client with `python3 src/client.py 127.0.0.1 8080`, where the first argument is the IP address of the server and the second one the listening port.

As soon as you launch the client, it will start sending some packets to the server.
The format of the packets is the following:
- 4 bytes for the length of the message (necessary since it's selected at random)
- A variable number of bytes for the message
- 1 byte for the checksum of the message

A percentage of them will have an (artificially) altered message, and the server should be able to spot the errors thanks to the checksum byte.

The console output of the server should be something like:
```
Received: Hello from client, Checksum: OK
Received: Hello from client, Checksum: OK
Received: ello, Checksum: ERROR
Received: Hllo from client, Checksum: ERROR
Received: ello world, Checksum: ERROR
Received: Hello world, Checksum: OK
Received: Hello frm client, Checksum: ERROR
Received: Hello frm client, Checksum: ERROR
Received: Hello from clint, Checksum: ERROR
Received: Hello, Checksum: OK
Received: Hello world, Checksum: OK
Received: Helo from client, Checksum: ERROR
Received: Helo from client, Checksum: ERROR
Received: Hell world, Checksum: ERROR
Received: ello from client, Checksum: ERROR
Received: Hello from client, Checksum: OK
```

Note that the server has a timeout on blocking socket operations of 5 seconds, after that it will gracefully close.
