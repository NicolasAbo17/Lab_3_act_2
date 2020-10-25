import socket
import struct
import sys
import time
import cv2
import numpy

import array as arr

import PySimpleGUI as sg

with open("properties.txt") as f:
    mylist = f.read().splitlines() 

NUMBERVIDEOS = int(mylist[0])
ports = [None] * 2
addresses = [None] * 2

for i in range(0, NUMBERVIDEOS ):
    addresses[i] = mylist[i+1]
    ports[i] = mylist[i+3]       

#default
number = 0

#multicast_group = input("please write the multicast_group ip")
#server_port = input("Please write the port number of the server")
<<<<<<< HEAD
sg.theme('DarkAmber')    # Keep things interesting for your users

layout = [[sg.Button('Video' + str(1), key='1')],      
          [sg.Button('Video' + str(2), key='2')]]      

window = sg.Window('Choose video', layout)      

while True:                             # The Event Loop
    event, values = window.read() 
    print(event, values)       
    number = int(event)
        break      

window.close()    

=======
for i in range(0, NUMBERVIDEOS ):
    layout =  [[sg.Button('Video' + str(i), key=i)]]
number = int(input("Please write the video number(1 or 2)"))
>>>>>>> main
multicast_group = addresses[number]
server = ('',int(ports[number]))

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server)

group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
BUF_LEN = 12000

while True:
    


    #total_pack, addr = soc.recvfrom(4)
    s=b""
    #soc.sendto(l.encode('ascii'),(addr[0],10004))
    #total_pack = int.from_bytes(total_pack,"little",signed=True)
    #print(total_pack)
    #for i in range(total_pack):
    data, addr = sock.recvfrom(BUF_LEN)
        #soc.sendto(l.encode('ascii'),(addr[0],10004))
    s += data
    frame = numpy.fromstring(s,dtype='uint8')
    frame = cv2.imdecode(frame,0)

    #COMENTAR DE ACA PARA ABAJO Y EJECUTAR REPRODUCE
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord ('q'):
        break
    #reproduce(frame)


def reproduce(frame):
    sg.theme("LightGreen")

    # Define the window layout
    layout = [
        [sg.Text("OpenCV Demo", size=(60, 1), justification="center")],
        [sg.Image(filename="", key="-IMAGE-")],
        [sg.Radio("None", "Radio", True, size=(10, 1))],
        [
            sg.Radio("threshold", "Radio", size=(10, 1), key="-THRESH-"),
            sg.Slider(
                (0, 255),
                128,
                1,
                orientation="h",
                size=(40, 15),
                key="-THRESH SLIDER-",
            ),
        ],
        [
            sg.Radio("canny", "Radio", size=(10, 1), key="-CANNY-"),
            sg.Slider(
                (0, 255),
                128,
                1,
                orientation="h",
                size=(20, 15),
                key="-CANNY SLIDER A-",
            ),
            sg.Slider(
                (0, 255),
                128,
                1,
                orientation="h",
                size=(20, 15),
                key="-CANNY SLIDER B-",
            ),
        ],
        [
            sg.Radio("blur", "Radio", size=(10, 1), key="-BLUR-"),
            sg.Slider(
                (1, 11),
                1,
                1,
                orientation="h",
                size=(40, 15),
                key="-BLUR SLIDER-",
            ),
        ],
        [
            sg.Radio("hue", "Radio", size=(10, 1), key="-HUE-"),
            sg.Slider(
                (0, 225),
                0,
                1,
                orientation="h",
                size=(40, 15),
                key="-HUE SLIDER-",
            ),
        ],
        [
            sg.Radio("enhance", "Radio", size=(10, 1), key="-ENHANCE-"),
            sg.Slider(
                (1, 255),
                128,
                1,
                orientation="h",
                size=(40, 15),
                key="-ENHANCE SLIDER-",
            ),
        ],
        [sg.Button("Exit", size=(10, 1))],
    ]

    # Create the window and show it without the plot
    window = sg.Window("OpenCV Integration", layout, location=(800, 400))

    while True:
        event, values = window.read(timeout=20)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if values["-THRESH-"]:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)[:, :, 0]
            frame = cv2.threshold(
                frame, values["-THRESH SLIDER-"], 255, cv2.THRESH_BINARY
            )[1]
        elif values["-CANNY-"]:
            frame = cv2.Canny(
                frame, values["-CANNY SLIDER A-"], values["-CANNY SLIDER B-"]
            )
        elif values["-BLUR-"]:
            frame = cv2.GaussianBlur(frame, (21, 21), values["-BLUR SLIDER-"])
        elif values["-HUE-"]:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frame[:, :, 0] += int(values["-HUE SLIDER-"])
            frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
        elif values["-ENHANCE-"]:
            enh_val = values["-ENHANCE SLIDER-"] / 40
            clahe = cv2.createCLAHE(clipLimit=enh_val, tileGridSize=(8, 8))
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])
            frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)

    window.close()
