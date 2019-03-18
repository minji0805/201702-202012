import socket
import argparse

def run_server(port=8888):
  host = ''
  
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()
    msg = conn.recv(1024)
    result = (msg.decode())
    print(f'{result[::-1]}')
    conn.sendall(msg)
    conn.close()

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Echo server -p port")
  parser.add_argument('-p', help="port_number", required=True)
  args = parser.parse_args()
  run_server(port=int(args.p))