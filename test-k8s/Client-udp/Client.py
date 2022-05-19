import socket
import os
import time

time.sleep(2)

msgFromClient       = "Hello UDP Server"
bytesToSend         = str.encode(msgFromClient)
#serverAddressPort   = ("127.0.0.1", 8011)
#serverAddressPort   = ("192.168.1.166", 8011)
#serverAddressPort = (os.environ['SERVER_IP'], 8011)
#serverAddressPort = (socket.gethostbyname("server-test-svc"), 8011)
serverAddressPort = (socket.gethostbyname(os.environ['SERVER_NAME']), 8011)

with open('clientOUT.txt' ,'a') as f:
    print("recuperato indirizzo server-service...", file=f)

bufferSize          = 1024
while(True):
    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = "Message from Server {}".format(msgFromServer[0])
    print(msg, msgFromServer[1])

    with open('clientOUT.txt' ,'a') as f:
        print(msg, msgFromServer[1], file=f)
    

    time.sleep(0.5)