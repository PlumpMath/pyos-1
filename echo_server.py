from socket import *
from pyos import *

def handle_client(client, addr):
    print "Connection from", addr
    while True:
        yield ReadWait(client)
        data = client.recv(65535)
        if not data:
            break
        yield WriteWait(client)
        client.send(data)

    client.close()
    print "client closed"


def server(port):
    print "Server start..."
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sock.bind(("", port))
    sock.listen(5)
    while True:
        yield ReadWait(sock)
        client, addr = sock.accept()
        yield NewTask(handle_client(client, addr))
