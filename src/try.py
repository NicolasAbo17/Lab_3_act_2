import socket
import cv2
import numpy
import time

host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 10002

#Create socet here
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host_ip, port))
#Get image size here
length, addr = s.recvfrom(16)
print(type(length))
see = int.from_bytes(length,"little",signed=True)
print("YUP",see)
