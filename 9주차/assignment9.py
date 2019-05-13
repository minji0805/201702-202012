import os
import socket
import argparse
import struct

ETH_P_ALL = 0x0003
ETH_SIZE = 14

def dumpcode(buf):
	print("\n")
	print('Raw Data')
	print("%7s"% "offset ", end='')

	for i in range(0, 16):
		print("%02x " % i, end='')

		if not (i%16-7):
			print("- ", end='')

	print("")

	for i in range(0, len(buf)):
		if not i%16:
			print("0x%04x" % i, end= ' ')

		print("%02x" % buf[i], end= ' ')

		if not (i % 16 - 7):
			print("- ", end='')

		if not (i % 16 - 15):
			print(" ")

	print("\n")

def make_ethernet_header(raw_data):
	ether = struct.unpack('!6B6BH', raw_data)
	print('Ethernet Header')
	if ether[12] != 2048:
		while True:
			if ether == 2048:
				break
	return {'[dst]':'%02x:%02x:%02x:%02x:%02x:%02x' % ether[:6],
		'[src]':'%02x:%02x:%02x:%02x:%02x:%02x' % ether[6:12],
		'[ether_type]':ether[12]}

def make_ip_header(raw_data2):
    print('\n')
    ip = struct.unpack('!BBHHBBBBH4B4B',raw_data2)
    print('IP HEADER')
    tmp = ip[0]
    tmp = bin(tmp)
    tmp = str(tmp)
    ip_ver = int(tmp[:-4], 2)
    ip_length = int(tmp[-4:], 2)
    return {'[version]' : ip_ver,
		'[header_length]' : ip_length*4,
		'[tos]': ip[1],
		'[total_length]' : ip[2],
		'[id]': ip[3],
		'[flag]': ip[4],
		'[offset]': ip[5],
		'[ttl]' : ip[6],
		'[protocol]' : ip[7],
		'[checksum]' : ip[8],
		'[src]':'%d:%d:%d:%d' % ip[9:13],
		'[dst]':'%d:%d:%d:%d' % ip[13:17]}

def ip_header_length(IP_SIZE):   
	IP_SIZE = hex(IP_SIZE)
	IP_TMP = int(str(IP_SIZE[3]))
	IP_TMP *= 32
	IP_TMP /= 8
	IP_SIZE = IP_TMP
	return IP_SIZE
	
def sniffing(nic):
	if os.name == 'nt':
		address_familiy = socket.AF_INET
		protocol_type = socket.IPPROTO_IP
	else:
		address_familiy = socket.AF_PACKET
		protocol_type = socket.ntohs(ETH_P_ALL)

	with socket.socket(address_familiy, socket.SOCK_RAW, protocol_type) as sniffe_sock:
		sniffe_sock.bind((nic, 0))

		if os.name == 'nt':
			sniffe_sock.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
			sniffe_sock.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

		data, _ = sniffe_sock.recvfrom(65535)
		ethernet_header = make_ethernet_header(data[:ETH_SIZE])

		for item in ethernet_header.items():
			print('{0} : {1}'.format(item[0], item[1]))

		IP_SIZE = ip_header_length(data[ETH_SIZE])
		IP_SIZE = IP_SIZE + ETH_SIZE

		ip_header = make_ip_header(data[ETH_SIZE:IP_SIZE])

		for item in ip_header.items():
			print('{0} : {1}'.format(item[0], item[1]))

		dumpcode(data)
        
		if os.name == 'nt':
			sniffe_sock.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='This is a simpe packet sniffer')
	parser.add_argument('-i', type=str, required=True, metavar='NIC', help='NIC')
	args = parser.parse_args()

	sniffing(args.i)
