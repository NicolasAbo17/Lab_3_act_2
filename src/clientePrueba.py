import socket
import cv2
import numpy
import time

host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 10003
BUF_LEN = 65540
#Create socet here
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind((host_ip, port))
#Get image size here
while True:
    total_pack, addr = soc.recvfrom(BUF_LEN)
    s=b""
    total_pack = int.from_bytes(total_pack,"little",signed=True)
    print("what the fuck?",total_pack)
    for i in range(total_pack):
        data, addr = soc.recvfrom(BUF_LEN)
        s += data
    frame = numpy.fromstring(s,dtype='uint8')
    frame = cv2.imdecode(frame,0)
    cv2.imshow('recv',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    