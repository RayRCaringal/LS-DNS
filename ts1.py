#Top-Level DNS 1

import sys
import os
import socket
import threading

#Stores Flag and Ip so it can be used in Key:Value pair dict 
class vals:
    def __init__(self,ip, flag):
        self.ip = ip
        self.flag = flag

def run():
    clientsocket.send(msg.encode('utf-8'))
    EOF = 1
    while EOF is not 0:
        print("[TS]: Waiting on Client")
        reply = clientsocket.recv(1024)
        hostName = reply.decode('utf-8').rstrip().lower()
        if hostName == "eof":
            print ("[TS]: Exiting a client at {}".format(addr))
            return
        print ("[TS]: Request from a client for hostname " + hostName)
        if hostName in table:
            print ("[TS]: Hostname " + hostName + " found sending IP Address " + table.get(hostName).ip + " to Client")
            clientsocket.send((table.get(hostName).ip).encode('utf-8'))
        else:
            print ("[TS]: Hostname " + hostName + " not found returning error")
            error = "Error:HOST NOT FOUND"
            clientsocket.send(error.encode('utf-8'))
    
#Creates Table 
table = {}
path = os.path.dirname(os.path.realpath('__file__')) + '/PROJI2-DNSTS1.txt'
if os.path.isfile(path):
    with open(path, 'r') as f:
        for line in f:
            items = line.split()
            val = vals(items[1], items[2])
            table[items[0]] = val

#Example on how to retrieve ip and flag 
#print(table.get("www.ibm.edu").ip)
#print(table.get("grep.cs.princeton.edu").flag)

#Create Server Socket
try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[TS]: Server socket created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()
server_binding = ('', int(sys.argv[1]))
ss.bind(server_binding)

#Listen forever 
msg = "[TS] Connected to Top-Level DNS"
while True:
    ss.listen(5)
    clientsocket, addr = ss.accept()
    print ("[TS]: Got a connection request from a client at {}".format(addr))
    #Acknowledgement 
    newThread = threading.Thread(target=run)
    newThread.start()


ss.close()
exit()
