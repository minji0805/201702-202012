import socket 
import argparse 
import glob 
import sys 
 
def run(host, port, f_name): 
     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
         s.connect(('127.0.0.1', 8888)) 
         filename = f_name
         s.sendall(filename.encode()) 
         data = s.recv(1024)
         print("file name : ", filename)
         print("contents of file : ", data.decode()) 

         if not data: 
             print("failed to find file.") 
             return 

         with open(f_name,'wb') as f: 
             try: 
                 f.write(data) 
                 data = s.recv(1024) 
             except Exception as e: 
                 print(e) 

         print("Transfer completed.")  
         print("List of files in the current directory : ") 
         file_list = glob.glob('*') 
         print(file_list) 
 
 
if __name__ == '__main__': 
    parser = argparse.ArgumentParser(description="Echo client -p port -i host -f f_name") 
    parser.add_argument('-p', help="port_number", required=True) 
    parser.add_argument('-i', help="host_name", required=True) 
    parser.add_argument('-f', help="file_name", required=True) 
    args = parser.parse_args() 
    run(host=args.i, port=int(args.p), f_name = args.f) 
