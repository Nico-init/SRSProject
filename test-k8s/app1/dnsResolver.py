import dns.resolver
import socket

#answers = dns.resolver.resolve('google.it', 'A')
answers = dns.resolver.resolve('server', 'A')
for rdata in answers:
    print("IP: ",rdata)

#funzione piu rapida di socket
print(socket.gethostbyname("server"))