
# Save as server.py
# Message Receiver
import os
from socket import *
import fcntl
import struct

def get_ip_address(ifname):
    s = socket(AF_INET, SOCK_DGRAM)
    return inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
    )[20:24])



Decoys = {
"decoy1" : "pcvm2-11.geni.uchicago.edu",
"decoy2" : "pcvm2-12.geni.uchicago.edu",
"decoy3" : "pcvm2-13.geni.uchicago.edu",
#"decoy4" : "pcvm3-6.vcu.instageni.net"
}


host = ""
port = 3000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)
print("Loading admin tool.")
while True:
    command = input("""
Here are the available commands \n
1) 1 G:Decoy - Get Specific Decoy Information 1-4 \n
2) 2 G:A - Get All Decoys information \n
3) 3 G:Decoy:Decoy - Compare State between two decoys \n
4) 4 G:O:Decoy:Decoy - Compare State between two decoy's offline\n
>""")
    
    print("Command: " , command)
    commandParts = command.split()
    print(commandParts, commandParts[0])
    if(commandParts[0] == '1'):
        #print("One decoy!")
        destination = commandParts[1].split(":")
        destination = destination[1]
        nexthost = Decoys[destination] # set to IP address of target computer
        nextport = 3000
        nextaddr = (nexthost, nextport)
        UDPSockSecond = socket(AF_INET, SOCK_DGRAM)
        data = str(get_ip_address('eth0')) + ":" + str(port)
        dataPacket = str.encode(data)
        #print(data , " \n \n " , dataPacket, "\n \n ", nextaddr)
        UDPSockSecond.sendto(dataPacket, nextaddr)
        #print("Got this far")
        (data, addr) = UDPSock.recvfrom(buf)
        print( "Received message: ", data)
    elif(commandParts[0] == '2'):
        for decoy in Decoys.values():
            nexthost = decoy # set to IP address of target computer
            nextport = 3000
            nextaddr = (nexthost, nextport)
            UDPSockSecond = socket(AF_INET, SOCK_DGRAM)
            data = str(get_ip_address('eth0')) + ":" + str(port)
            dataPacket = str.encode(data)
            UDPSockSecond.sendto(dataPacket, nextaddr)
            (data, addr) = UDPSock.recvfrom(buf)
            print( "Received message from: ", nexthost, "and the data was: " , data)
    elif(commandParts[0] == '3'):
        print(3)
    elif(commandParts[0] == '4'):
        print(4)
    elif(commandParts[0] == 'exit'):
        break;
    else:
        print("rip")
    #(data, addr) = UDPSock.recvfrom(buf)
    #print( "Received message: ", data)




UDPSock.close()
os._exit(0)


