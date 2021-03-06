import socket
from datetime import datetime, timedelta


class Client:
    def __init__(self, addr):
        self.addr = addr
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(addr)
        self.finish_time = datetime.now()

    def send_recv(self, msg):
        self.socket.send(msg.encode())
        self.finish_time += timedelta(seconds=int(msg[1]))
        data = self.socket.recv(1024).decode()
        return data