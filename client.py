#Client
#Use PROJI2-DNSTS1.txt and PROJI2-DNSTS2.txt for tables
#Use PROJI2-HNS.txt for searches
#DNS entry/host name are MAX 200 chars 
#DNS look ups are case insensitive
#python client.py lsHostname lsListenPort
#lsHostname argv[1]
#lsListenPort arv[2]



#CHANGES
# Client only requests to LS

import sys
import os
import socket

try:
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[C]: Client socket created")
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()
        
# Define the port on which you want to connect to the server
lsHostname = sys.argv[1]
lsListenPort = int(sys.argv[2])

LS_addr = ""
if lsHostname is "localhost":
    LS_addr = socket.gethostbyname(socket.gethostname())
else:
    LS_addr = socket.gethostbyname(lsHostname)

lsServer_binding = (LS_addr, lsListenPort)

#Connect to Load Balancing Server
cs.connect(lsServer_binding)

#Receive Acknowledgement 
msg = cs.recv(1024)
print("[C]: Data received from server: {}".format(msg.decode('utf-8')))

#Create the File Path as Read 
path = os.path.dirname(os.path.realpath('__file__')) + '/PROJI2-HNS.txt'
if os.path.isfile(path):
    with open(path, 'r') as f:
        result = ""

        #Begin Search Storing Text in Result 
        for address in f:
            print("[C]: Searching for hostname " + address.rstrip())
            result += address.rstrip()

            #Send Hostname to Load Balancing Server
            cs.send(address.encode('utf-8'))
            msg = cs.recv(1024).decode('utf-8') 
            table = msg.split()

            #Check For Results

        msg = "EOF"
        cs.send(msg.encode('utf-8'))
        print("[C]: Creating text file")
        f = open("RESOLVED.TXT", 'w')
        f.write(result)
        f.close()

print("[C]: Closing Sockets")
cs.close()
exit()


