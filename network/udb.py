http www 80
ftp file transport 21
smtp mail
port 0~65535
port 0~1023 has been used
dynamic port 1024~65535

Intenational Protocal Suite
tcp/ip protocal

socket api client-server(cs model)

import socket
socket.socket(AddressFamily, Type)
AddressFamily: AF_INET(internet), AF_UNIX(localhost)
Type:SOCK_STREAM(tcp), SOCK_DGRAM(udp)

udp --user data protocal ----no connect, fast, inreliable
tcp --transmission control protocal --connect --transfer and receive on same time

'''udp send'''
from socket import *

# creat object
udpsocket = socket(AF_INET, SOCK_DGRAM)
# set the ip addr
sendAddr = ('127.0.0.1', 9999)
# send message
udpsocket.sendto(b'message', sendAddr)
# close the object
udpsocket.close()

'''udp receive'''
from socket import *

udpso = socket(AF_INET, SOCK_DGRAM)
sendAddr = ('192.168.137.137', 8080)
udpso.sendto(b'message', sendAddr)
# 1024 is the max receive bits
receivedata = udpso.recvfrom(1024)
udpsoc.close()

'''set default parameter of udp'''
from socket import *
s = socket(AF_INET, SOCK_DGRAM)
ip = ('', 7788)
# bind the ip
s.bind(ip)


'''echo server'''
from socket import *

s = socket(AF_INET, SOCK_DGRAM)
ip = ('', 9999)
s.bind(ip)
num = 0
while True:
    recfdata = s.recvfrom(1024)
    s.sendto(recfdata[0], recfdata[1])
    print('This is %d information'%num)
    num += 1
s.close()

bytes(message, encoding='utf-8')
