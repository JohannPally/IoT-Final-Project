import socket
from dispenser import Dispense
from dog_detection import Vision
from sound import Sound
from history import History

HOST = "192.168.50.217" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

from bluedot.btcomm import BluetoothServer
from signal import pause

disp = Dispense()
vis = Vision()
snd = Sound()
hist = History()

def received_handler(data):
    global disp
    trts = disp.act() 
    if trts is not None:
        mess = f"Nova has been given {trts} treats so far!".encode('ascii')
        s.send(mess)
    
s = BluetoothServer(received_handler)

while True:
    input()
    message= f"alert test".encode('ascii')
    s.send(str(message))

pause()

while False:
    #VISION
    det = vis.check_dog()

    #SOUND
    smp = snd.get_sample()

    #HISTORY
    hist.add_position(det)
    hist.add_sample(smp)

    if hist.check_noise():
        message= f"NOISE alert".encode('ascii')
        s.send(str(message))
    if hist.check_spaz():
        message= f"MOVEMENT alert".encode('ascii')
        s.send(str(message))


# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     disp = Dispense()
#     vis = Vision()
#     snd = Sound()
#     hist = History()


#     try:
#         while 1:
            

#             #MESSAGING
#             client, clientInfo = s.accept()
#             print("server recv from: ", clientInfo)

#             #DO ALERTS
#             mess = hist.check_noise()
#             if mess is not None:
#                 message = f"{mess}".encode('ascii')
#                 client.sendall(message)

#             mess = hist.check_spaz()
#             if mess is not None:
#                 message = f"{mess}".encode('ascii')
#                 client.sendall(message)

#             data = client.recv(1024) 
#             if data == b'stop':
#                 print("Stopping socket")
#                 client.close()
#                 s.close()
#                 break
#             if data != b"":
#                 trts = disp.act(data)
#                 message= f"Nova has had {trts} treats!".encode('ascii')
#                 client.sendall(message) # Echo back to client
            
#     except Exception as e:
#         print('error: ', e)
#         print("Closing socket")
#         client.close()
#         s.close()