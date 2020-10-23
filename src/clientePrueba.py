import socket
import cv2
import numpy
import time

host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 10002
BUF_LEN = 7700
#Create socet here
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind((host_ip, port))
cont = 0
#Get image size here
l = 'a'
while True:
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