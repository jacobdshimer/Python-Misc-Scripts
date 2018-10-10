import socket
import time

ip = "127.0.0.1"
port = "135"

retry = 5
delay = 10
timeout = 3

def isOpen(ip, port, timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    if sock.connect_ex((ip, int(port))) == 0:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        print(str(port) + ":" + "Open")
        return True
    else:
        sock.close()
        print(str(port) + ":" +  "Closed")
        return False


if __name__ == "__main__":
    print("What is the IP address you would like to port scan?")
    ip = input("> ")
    print("What is the start port?")
    startPort = int(input("> "))
    print("What is the end port?")
    endPort = int(input("> "))
    timeout = 3
    for port in range(startPort, endPort):
        isOpen(ip, port, timeout)
