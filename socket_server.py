#coding=gbk
import socket

BUFFER_SIZE = 4096
PORT = 21111

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(('localhost', PORT))#�󶨵���ip��ַ
    sock.listen()#��ʼ���������д���ʱ��������ʾ�����ͬʱ�������û��ˣ�������û��˻��Ŷ�

    while True:
        connection, address = sock.accept()#����[ip�׽��֣� ��������ַ�� �˿ڣ�]���˿�ÿ�η��ز�һ��
        with connection:
            print('���ӣ�{}'.format(address))

            while True:
                data = connection.recv(BUFFER_SIZE)#�����׽���
                if not data:
                    break

                if data.decode().strip() == 'stop':#���ͻ��˷��ص��ǹر���Ϣʱ��ȥ����β�ո�
                    connection.sendall('gg'.encode())#��ͻ��˴����׽���
                    connection.shutdown(1)#�ر�socket�Ķ�д���ܣ�0�رն���1�ر�д��2���ر�
                    connection.close()#�ͷ�Socketռ�õ�������Դ�����ҹرո�����
                    exit()

                connection.sendall(data)#��ͻ��˴����׽���
