import socket 
import argparse 
import os 
import glob
 
def run_server(port=8888,file_dir = 0): 
      host = '127.0.0.1' 
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
        s.bind((host,port)) 
        s.listen(1) 
        conn, addr = s.accept() 
        filename = conn.recv(1024) 
        filename = filename.decode() 
        dir = file_dir + filename
        print("file name : ", filename)
        print("size : " , os.path.getsize(dir)) 

        with open(file_dir + filename, 'rb') as f: 
            try: 
                data = f.read(1024) 
                conn.sendall(data) 
                print("Transfer completed.") 
            except Exception as e: 
                print(e) 
        conn.close() 
 
 
if __name__ == '__main__': 

    print("List of files in the current directory : ") 
    file_list = glob.glob('*') 
    print(file_list)

    parser = argparse.ArgumentParser(description="Echo server -p port -d file_dir") 
    parser.add_argument('-p',help="port_number",required=True) 
    parser.add_argument('-d',help="directory",required=True) 
    args = parser.parse_args() 
    run_server(port=int(args.p) , file_dir=args.d) 
