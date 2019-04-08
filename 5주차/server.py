import socket
import threading
import argparse

def socket_handler(conn):
    msg = conn.recv(1024)
    rev_msg = msg[::-1]
    conn.sendall(rev_msg)
    print(addr[0], " : closed")
    conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Thread server -p port")
    parser.add_argument('-p', help = "port_number", required = True)

    args = parser.parse_args()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', int(args.p)))
    server.listen(5)

    while True:
        conn, addr = server.accept()
        receiver = threading.Thread(target=socket_handler, args=(conn,))
        receiver.start()
        print("connected to :", addr[0], ":", addr[1])
    server.close()
