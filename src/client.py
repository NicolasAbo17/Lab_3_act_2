import socket, struct, cv2, pickle
import pyshine as ps
import imutils
import struct
import sys


multicast_group = '224.3.29.71'
server_address = ('', 10000)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to
# the multicast group on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_ADD_MEMBERSHIP,
    mreq)

# Receive/respond loop
while True:
    try:
        if sock:
            data = b""
            payload_size = struct.calcsize("Q")
            while True:
                while len(data) < payload_size:
                    packet = sock.recv(4 * 1024)  # 4K
                    if not packet: break
                    data += packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q".packed_msg_size)[0]

                while len(data) < msg_size:
                    data += sock.recv(4 * 1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                text = f"CLIENT:"
                frame = ps.putBText(frame, text, 10, 10, vspace=10, hspace=1, font_scale=.7,
                                    background_RGB=(255, 0, 0), text_RGB=(255, 250, 250))
                cv2.imshow(f"FROM ", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
            sock.close()
    except Exception as e:
        print("Cliente desconectado")
        pass
    finally:
        print('Socket cerrado')
        sock.close()