import socket
import cv2
import numpy
import time

host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 10002
BUF_LEN = 4096
#Create socet here
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind((host_ip, port))
cont = 0
#Get image size here
while True:
    soc.sendall(cont)
    cont = cont +1
    total_pack, addr = soc.recvfrom(4)
    s=b""
    total_pack = int.from_bytes(total_pack,"little",signed=True)
    print(total_pack)
    for i in range(total_pack):
        data, addr = soc.recvfrom(BUF_LEN)
        s += data
        print(data)
    frame = numpy.fromstring(s,dtype='uint8')
    frame = cv2.imdecode(frame,0)
    cv2.imshow('frame',frame)
