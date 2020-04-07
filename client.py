#client
#Use PROJI-DNSRS.txt and PROJI-DNSTS.txt for tables 
#Use PROJI-HNS.txt for searches
#If "A" return else check TS if still NS return error 
#DNS entry/host name are MAX 200 chars 
#DNS look ups are case insensitive 

#python client.py rsHostname rsListenPort tsListenPort
#rsHostname argv[1]

import sys
import os
import time
import random
import socket

try:
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cs2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[C]: Client socket created")
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()
        
# Define the port on which you want to connect to the server
rsHostname = sys.argv[1]
rsListenPort = int(sys.argv[2])
tsListenPort = int(sys.argv[3])
RS_addr = ""
if rsHostname is "localhost":
    RS_addr = socket.gethostbyname(socket.gethostname())
else:
    RS_addr = socket.gethostbyname(rsHostname)

tsConnected = 0
rsServer_binding = (RS_addr, rsListenPort)

#Connect to Root Server first 
cs.connect(rsServer_binding)

#Receive Acknowledgement 
msg = cs.recv(1024)
print("[C]: Data received from server: {}".format(msg.decode('utf-8')))

#Create the File Path as Read 
path = os.path.dirname(os.path.realpath('__file__')) + '/PROJI-HNS.txt'
if os.path.isfile(path):
    with open(path, 'r') as f:
        result = ""

        #Begin Search Storing Text in Result 
        for address in f:
            print("[C]: Searching for hostname " + address.rstrip())
            result += address.rstrip()

            #Send Hostname to Root Server 
            cs.send(address.encode('utf-8'))
            msg = cs.recv(1024).decode('utf-8') 
            table = msg.split()

            #Address not in RS check TS 
            if table[0] == "[NS]":
                print("[C]: Address not found in Root Server, entering Top-Level DNS: " + table[1])
                
                #Connect to TS if not Connected 
                if tsConnected is 0:
                    if table[1] == "localhost":
                        TS_addr = socket.gethostbyname(socket.gethostname())
                    else:
                        TS_addr = socket.gethostbyname(table[1])
                    tsServer_binding = (TS_addr, tsListenPort)
                    cs2.connect(tsServer_binding)
                    tsConnected = 1
                    msg = cs2.recv(1024)
                    print("[C]: Data received from server: {}".format(msg.decode('utf-8')))

                #Send Address to TS and Check Response     
                cs2.send(address.encode('utf-8'))
                msg = cs2.recv(1024).decode('utf-8')
                if msg == "Error:HOST NOT FOUND":
                    print("[C]: Address not found saving Error to RESOLVED.txt")
                    result += " - Error:HOST NOT FOUND\n"
                else:
                    print("[C]: Address found saving IP Address " + table[0] + " to RESOLVED.txt")
                    result += " " + msg + " A\n"

            #IP Address found in the RS        
            else:
                print("[C]: Address found saving IP Address " + table[0] + " to RESOLVED.txt")
                result += " " + table[0] + " A\n"
        msg  = "EOF"
        cs.send(msg.encode('utf-8'))
        if tsConnected is 1:
            cs2.send(msg.encode('utf-8'))
        print("[C]: Creating text file")
        f = open("RESOLVED.TXT", 'w')
        f.write(result)
        f.close()

print("[C]: Closing Sockets")
cs.close()
cs2.close()
exit()


