import socket

## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)

#localIP     = "127.0.0.1"
localIP     = "0.0.0.0"
#localIP     = ip_address

localPort   = 8011
bufferSize  = 1024

msgFromServer       = "Hello UDP Client from:{}".format(ip_address)
bytesToSend         = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("I'm Server: ", hostname, "IP: ", ip_address)
print("UDP server up and listening. IP: ", localIP, "PORT: ", localPort)
print()

with open('serverOUT.txt' ,'a') as f:
    print("I'm Server: ", hostname, "IP: ", ip_address, file=f)
    print("UDP server up and listening. IP: ", localIP, "PORT: ", localPort, file=f)
    print(file=f)

 

# Listen for incoming datagrams
while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    
    print(clientMsg)
    print(clientIP)

    with open('serverOUT.txt' ,'a') as f:
        print(clientMsg, file=f)
        print(clientIP, file=f)

    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)