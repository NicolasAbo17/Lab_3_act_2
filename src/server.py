import socket, struct, cv2, pickle, threading
import imutils
import struct
import sys
import pyshine as ps

multicast_group = ('224.3.29.71', 10000)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket.SOCK_DGRAM)

# Set a timeout so the socket does not block
# indefinitely when trying to receive data.

# sock.settimeout(0.2)

# Set the time-to-live for messages to 1 so they do not
# go past the local network segment.

ttl = struct.pack('b', 1)
#sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

# Bind to the server address
host_name = socket.gethostname()

# NPI
#sock.bind((host_name, 10000))

host_ip = socket.gethostbyname(host_name)
print("HOST IP:", host_ip)
print("Listening at:", multicast_group)

# Receive/respond loop
while True:
    try:
        video = cv2.VideoCapture('../videos/guiltygear.mp4')
        img, frame = video.read()
        frame = imutils.resize(frame, width=380)
        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a)) + a
        #client_socket.sendall(message)

        sock.sendto(message, multicast_group)
        # cv2.imshow(f'TO: {multicast_group[0]}, frame')
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            sock.close()
    except Exception as e:
        print(e)
        print("Transmisión terminada")
        break