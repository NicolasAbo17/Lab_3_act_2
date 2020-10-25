import socket
import struct
import sys

multicast_group = input("please write the multicast_group ip")
server_port = input("Please write the port number of the server")
server = ('',server_port)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server)

group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
BUF_LEN = 7700

cont = cont +1
    #total_pack, addr = soc.recvfrom(4)
    s=b""
    #soc.sendto(l.encode('ascii'),(addr[0],10004))
    #total_pack = int.from_bytes(total_pack,"little",signed=True)
    #print(total_pack)
    #for i in range(total_pack):
    data, addr = soc.recvfrom(BUF_LEN)
        #soc.sendto(l.encode('ascii'),(addr[0],10004))
    s += data
    frame = numpy.fromstring(s,dtype='uint8')
    frame = cv2.imdecode(frame,0)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord ('q'):
        break
