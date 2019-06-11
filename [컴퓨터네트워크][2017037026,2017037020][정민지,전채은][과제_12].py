import argparse
import struct
import socket
import sys
import random
import time
from functools import reduce

SOURCE_PORT = 8888
DESTIN_PORT = 33434
ETH_P_ALL = 0x0003
ETH_SIZE = 14
IP_SIZE = 20            
ICMP_SIZE = 8           
UDP_SIZE = 8             
ICMP_ECHO_REQUEST = 8  

class Parsing():
    def parsing_ip_header(self, data) :
        iph = struct.unpack('!BBHHHBBH4s4s',data)
        return {
        'version' : iph[0]<<4,                
        'header_length' :iph[0]&0b00001111,           
        'tos': iph[1],
        'total_length' :iph[2],
        'id' :iph[3],
        'flag_offset' : iph[4],
        'ttl' : iph[5],
        'protocol' : iph[6],
        'chksum' : iph[7],
        'src' : '%d.%d.%d.%d' % iph[8:12],
        'dst' : '%d.%d.%d.%d' % iph[12:]
        }

    def parsing_icmp_message(self, data) :
        icmph = struct.unpack('!bbHHhH', data)
        return {
        'type' : icmph[0],
        'code' : icmph[1],
        'chksum' : icmph[2],
        'null' : icmph[3]
        }

    def parsing_icmp_header(self, data) :
        icmph = struct.unpack('!bbHHhH',data)
        return {
        'type' : icmph[0],
        'code' : icmph[1],
        'chksum' : icmph[2],
        'id' : icmph[3],
        'seq' : icmph[4],
        'data' : icmph[5:]
        }    

    def parsing_udp_header(self, data) :
        udph = struct.unpack('!HHHH', data)
        return {
        'src_port' : udph[0],
        'dst_port' : udph[1],
        'length' : udph[2],
        'chksum' : udph[3],
        'data' : udph[4:]
        }

def chksum (header) :
    size = len(header)
    if (size % 2) == 1:
        header += b'\x00'
        size += 1

    size = size // 2
    header = struct.unpack('!' + str(size) + 'H', header)
    sum = reduce(lambda x, y : x+y, header)
    chksum = (sum >> 16) + (sum & 0xffff)
    chksum += chksum >> 16
    chksum = (chksum ^ 0xffff)

    return struct.pack('!H', chksum)

class IPPacket() :
    def __init__(self, protocol, dst='127.0.0.1', src='0.0.0.0', ttl = 1) :
        self.dst = dst 
        self.src = src 
        self.ip_ttl = ttl 
        self.raw = None 
        self.ip_field_list() 

    def create_ip_field_list(self) : 
        ip_version = 4 
        ip_headerlen = 5 
 
        self.ip_ver = (ip_version << 4 ) + ip_headerlen
        ip_dsc = 0 
        ip_ecn = 0 
 
        self.ip_dfc = (ip_dsc << 2 ) + ip_ecn 
        self.ip_total_len = 80 
        self.ip_id = 54321 
 
        ip_resv = 0 
        ip_dtf = 0 
        ip_mrf = 0 
        ip_frag_offset = 0 

        self.ip_flag = (ip_resv << 7) + (ip_dtf << 6) + (ip_mrf << 5) + (ip_frag_offset) 
        self.ip_protocol = socket.IPPROTO_ICMP 
        self.ip_chksum = 0 
        self.ip_send_addr = socket.inet_aton(self.src) 
        self.ip_des_addr = socket.inet_aton(self.dst) 
        
        return 


    def ip_field_list(self) :
        self.raw = struct.pack('!BBHHHBBH4s4s',
        self.ip_ver,   
        self.ip_dfc,    
        self.ip_total_len,   
        self.ip_id,   
        self.ip_flag,   
        self.ip_ttl,   
        self.ip_protocol,  
        self.ip_chksum,   
        self.ip_send_addr,  
        self.ip_des_addr  
    ) 
        return self.raw

class ICMPPacket:
    def __init__(self,
        icmp_type = ICMP_ECHO_REQUEST,
        icmp_code = 0,
        icmp_chksum = 0,
        icmp_id = 0,
        icmp_seq = 0,
        icmp_data = 1,
        ):

        self.icmp_type = icmp_type 
        self.icmp_code = icmp_code 
        self.icmp_chksum = icmp_chksum 
        self.icmp_id = icmp_id 
        self.icmp_seq = icmp_seq 
        self.icmp_data = icmp_data 
        self.raw = None 
        self.create_icmp_field_list() 
 
    def create_icmp_field_list(self): 
        self.raw = struct.pack('!bbHHhH',
 	        self.icmp_type, 
            self.icmp_code, 
            self.icmp_chksum, 
            self.icmp_id, 
            self.icmp_seq, 
            self.icmp_data, 
            ) 
        self.icmp_data_pack = struct.pack
         
        self.icmp_chksum = self.icmp_chksum(self.raw) 
        self.raw = struct.pack('!bbHHhH',
 	    	self.icmp_type, 
 	    	self.icmp_code, 
 	    	self.icmp_chksum, 
 	    	self.icmp_id, 
 	    	self.icmp_seq, 
            self.icmp_data, 
             	) 
        return  

class UDPPacket:
    def __init__(self, udp_src_port, udp_dst_port) :
        self.udp_src_port = udp_src_port
        self.udp_dst_port = udp_dst_port
        self.length = 8
        self.chksum = 0
        self.raw = None

    def create_udp_field_list(self) :
        self.raw = struct.pack('!HHHH',
        self.udp_src_port,
        self.udp_dst_port,
        self.length,
        self.chksum,
        )

        return self.raw

def traceroute (dst_addr, packet_size , proto, maximum_hop, timeout, dst_port) :
    global dst, data_size
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW) :
        socket.socket.bind(('', SOURCE_PORT))
        
        sniff_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sniff_sock.bind(('', SOURCE_PORT))

        sniff_sock.settimeout(float(timeout))          

        dst = socket.inet_aton(dst_addr)

        if proto == socket.IPPROTO_ICMP :               
            data_size = packet_size - IP_SIZE - ICMP_SIZE
        elif proto == socket.IPPROTO_UDP :
            data_size = packet_size - IP_SIZE - UDP_SIZE

        sniff_sock.close()

if __name__ == "__main__":
    args = parser.parse_args() 
    parser = argparse.ArgumentParser(description='Traceroute')
    parser.add_argument('address', type=str, help = 'Destination IP')
    parser.add_argument('size', type=int, help = 'Size')

    proto_group = parser.add_mutually_exclusive_group()
    proto_group.add_argument('-I',  const = socket.IPPROTO_ICMP, default = socket.IPPROTO_ICMP, help = 'ICMP')
    proto_group.add_argument('-U',  const = socket.IPPROTO_UDP, help = 'UDP')

    parser.add_argument('-t', type=int, required = False, help = 'Time Out')
    parser.add_argument('-p', type=int, required = False, default = DESTIN_PORT ,help = 'Destination Port')
    parser.add_argument('-c', type=int, required = False, help = 'Maximum Hops')

    dst = '0.0.0.0'
    src = '0.0.0.0'
    data_size = 0

    if args.U :
        traceroute(args.address, args.size, args.U, args.c, args.t, args.p)
    else :
        traceroute(args.address, args.size, args.I, args.c, args.t, args.p)
