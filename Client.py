import socket


class Client:
    def __init__(self, addr):
        self.addr = addr
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(addr)

    def send_recv(self, msg):
        print('Client sent to ' + str(self.addr) + ': ' + msg)
        self.socket.send(msg.encode())
        data = self.socket.recv(1024).decode()
        print('Client received from ' + str(self.addr) + ': ' + data)
        return data