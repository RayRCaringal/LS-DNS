#python ls.py lsListenPort ts1Hostname ts1ListenPort ts2Hostname ts2ListenPort


import sys
import socket
import threading

# Stores Flag and Ip so it can be used in Key:Value pair dict
class vals:
    def __init__(self, ip, flag):
        self.ip = ip
        self.flag = flag

#Using

#If Not Found send [NF], use this because we want to catch the timeout exception
def inTS(hostName, sock):
    sock.send(hostName.encode('utf-8'))
    try:
        msg = sock.recv(1024)
        return msg
    except socket.error as err:
        return "[NF]"

def run():
    clientsocket.send(msg.encode('utf-8'))
    EOF = 1
    while EOF != 0:
        print("[LS]: Waiting on Client")
        reply = clientsocket.recv(1024)
        hostName = reply.decode('utf-8').rstrip()
        if hostName == "EOF":
            print("[LS]: Exiting a client at {}".format(addr))
            return
        else:
            print("[LS]: Request from a client for hostname " + hostName)
            one = inTS(hostName, ls1)
            two = inTS(hostName, ls2)
            if one == "[NF]" and two == "[NF]":
                print("[LS]: Hostname " + hostName + " not found returning error")
                error = "Error:HOST NOT FOUND"
                clientsocket.send(error.encode('utf-8'))
            elif one == "[NF]":
                clientsocket.send(two)
            elif two == "[NF]":
                clientsocket.send(one)

def getHost(addr):
    if addr == "localhost":
        return socket.gethostname()
    else:
        return addr



# Create Server Socket
try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ls1= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ls2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[LS]: Server socket created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()

#Bind Sever to Port
server_binding = ('', int(sys.argv[1]))

#Define Ports and Hostnames
ts1HostName = sys.argv[2]
ts2HostName = sys.argv[4]
ts1Port = (int(sys.argv[3]))
ts2Port = (int(sys.argv[5]))

TS1_addr = socket.gethostbyname(getHost(ts1HostName))
TS2_addr = socket.gethostbyname(getHost(ts2HostName))

ts1Server_binding = (TS1_addr, ts1Port)
ts2Server_binding = (TS2_addr, ts2Port)

#Connect to Top-Level DNS 1
ls1.connect(ts1Server_binding)
ls2.connect(ts2Server_binding)

#Receive Acknowledgement
msg1 = ls1.recv(1024)
msg2 = ls2.recv(1024)
print("[LS]: Data received from server: {}".format(msg1.decode('utf-8')))
print("[LS]: Data received from server: {}".format(msg2.decode('utf-8')))

#Set Socket Timeouts
ls1.settimeout(5)
ls2.settimeout(5)


ss.bind(server_binding)
# Listen forever
msg = "[LS] Connected to Load Balancing Server"
while True:
    ss.listen(5)
    clientsocket, addr = ss.accept()
    print("[LS]: Got a connection request from a client at {}".format(addr))
    newThread = threading.Thread(target=run)
    newThread.start()

ss.close()
exit()
