from Client import Client
import socket
import threading

HOST = '10.0.0.1'  # Standard loopback interface address (localhost)
PORT = 80       # Port to listen on (non-privileged ports are > 1023)


def choose_server():
    return servers_connections[0]


def handle_client(conn, addr):
    with conn:
        print('Connected by', addr)
        data = conn.recv(1024).decode()
        if data:
            print('LB received from ' + str(addr) + ': ' + data)
            # msg_type = data[0]
            # msg_len = data[1]

            connection = choose_server()
            print('LB sent to ' + str(connection.addr) + ': ' + data)
            msg = connection.send_recv(data)
            conn.send(msg.encode())


def run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            client_thraed = threading.Thread(target=handle_client, kwargs={"conn": conn, "addr": addr})
            client_thraed.start()


if __name__ == "__main__":
    addrList = [("192.168.0.101", 80), ("192.168.0.102", 80), ("192.168.0.103", 80)]
    servers_connections = [Client(addr) for addr in addrList]
    for server_conn in servers_connections:
        server_conn.connect()
    run()