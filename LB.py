from Client import Client
import socket
import threading
from datetime import timedelta

HOST = '10.0.0.1'  # Standard loopback interface address (localhost)
PORT = 80  # Port to listen on (non-privileged ports are > 1023)


def choose_server(msg_type, msg_len):
    execution_times = []
    if msg_type == 'M':
        execution_times = [2 * msg_len, 2 * msg_len, msg_len]
    elif msg_type == 'V':
        execution_times = [msg_len, msg_len, 3 * msg_len]
    elif msg_type == 'P':
        execution_times = [msg_len, msg_len, 2 * msg_len]
    current_times = [server.finish_time for server in servers_connections]
    finish_times = [current + timedelta(seconds=execution) for execution, current in
                    zip(execution_times, current_times)]
    min_index = 0
    min_value = finish_times[0]
    for i in range(1, len(finish_times)):
        if finish_times[i] < min_value:
            min_value = finish_times[i]
            min_index = i
    return servers_connections[min_index]


def handle_client(conn, addr):
    print('Connected by', addr)
    data = conn.recv(1024).decode()
    if data:
        msg_type, msg_len = data[0], int(data[1])

        connection = choose_server(msg_type, msg_len)
        print('LB will send to server ' + str(connection.addr) + ': ' + data + ', that came from ' + str(addr))
        msg = connection.send_recv(data)
        conn.send(msg.encode())
    conn.close()


def run():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        client_thraed = threading.Thread(target=handle_client, kwargs={"conn": conn, "addr": addr})
        client_thraed.start()


if __name__ == "__main__":
    addrList = [("192.168.0.101", 80), ("192.168.0.102", 80), ("192.168.0.103", 80)]
    servers_connections = [Client(addr) for addr in addrList]
    run()
