#coding=gbk
import socket
import sys

BUFFER_SIZE = 4096 #��������С������򷵻ض����ܳ����ô�С
prot = 21111

if len(sys.argv) > 1:
    prot = sys.argv[1]

maya_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#STREAM����ʽ�׽��֣�����ȫ��DGRAM�������׽��֣��죬���ȶ�
maya_socket.connect(('localhost', prot))

maya_socket.sendall("stop".encode())#py2�¿���ֱ�����ַ�����py3����Ҫ���ַ����������.encode()
print(maya_socket.recv(BUFFER_SIZE).decode())#py2�¿���ֱ�Ӵ�ӡ��py3����Ҫ����.decode()

maya_socket.close()
