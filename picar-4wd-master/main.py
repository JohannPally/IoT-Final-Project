import socket
from dispenser import Dispense
from dog_detection import Vision
from sound import Sound
from history import History

HOST = "192.168.50.217" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    disp = Dispense()
    vis = Vision()
    snd = Sound()
    hist = History()


    try:
        while 1:
            #VISION
            det = vis.check_dog()

            #SOUND
            smp = snd.get_sample()

            #HISTORY
            hist.add_position(det)
            hist.add_sample(smp)

            #MESSAGING
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)

            #DO ALERTS
            mess = hist.check_noise()
            if mess is not None:
                message = f"{mess}".encode('ascii')
                client.sendall(message)

            mess = hist.check_spaz()
            if mess is not None:
                message = f"{mess}".encode('ascii')
                client.sendall(message)

            data = client.recv(1024) 
            if data == b'stop':
                print("Stopping socket")
                client.close()
                s.close()
                break
            if data != b"":
                trts = disp.act(data)
                message= f"Nova has had {trts} treats!".encode('ascii')
                client.sendall(message) # Echo back to client
            
    except Exception as e:
        print('error: ', e)
        print("Closing socket")
        client.close()
        s.close()