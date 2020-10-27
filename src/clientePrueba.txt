import socket
import cv2
import numpy
import time
import struct

MCAST_GRP = input("ip number of the group ")
MCAST_PORT = int(input("port number of the group "))
IS_ALL_GROUPS = True

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if IS_ALL_GROUPS:
    # on this port, receives ALL multicast groups
    sock.bind(('', MCAST_PORT))
else:
    # on this port, listen ONLY to MCAST_GRP
    sock.bind((MCAST_GRP, MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
BUF_LEN = 12000
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    s=b""
    data, addr = sock.recvfrom(BUF_LEN)
        #soc.sendto(l.encode('ascii'),(addr[0],10004))
    s += data
    frame = numpy.fromstring(s,dtype='uint8')
    frame = cv2.imdecode(frame,0)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord ('q'):
        break
