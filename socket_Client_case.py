#coding=gbk
import socket
import traceback
import json
import time


class ClientBase(object):
    """
    �ͻ���
    """
    PORT = 20201 #�˿�
    HEADER_SIZE = 10  #��������С

    def __init__(self, timeout=2):
        self.timeout = timeout#������Ϣ��ĵȴ�ʱ��
        self.port = self.__class__.PORT

        self.discard_count = 0

    def connect(self, port=-1):
        if port >= 0:
            self.port = port
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('localhost', self.port))  #���ӵ��˿�
            self.client_socket.setblocking(0)#����Ϊ������ģʽ������recv()û�з����κ����ݽ�����socket.error�쳣
        except:
            traceback.print_exc()
            return False

        return True

    def disconnect(self):
        try:
            self.client_socket.close()
        except:
            traceback.print_exc()
            return False

        return True

    def send(self, cmd):
        json_cmd = json.dumps(cmd)#�ֵ�תjson����
        message = []
        message.append('{}'.format(len(json_cmd.encode())).zfill(ClientBase.HEADER_SIZE))
        message.append(json_cmd)

        try:
            msg_str = ''.join(message)
            self.client_socket.sendall(msg_str.encode())#��˿ڷ�����Ϣ
        except:
            traceback.print_exc()
            return None

        return self.recv()

    def recv(self):
        """
        ��ȡ����
        :return:
        """
        total_data = []
        data = ''
        reply_length = 0
        bytes_remaining = ClientBase.HEADER_SIZE

        start_time = time.time()
        while time.time() - start_time < self.timeout:#���ڵȴ�ʱ����
            try:
                data = self.client_socket.recv(bytes_remaining)#��ȡָ�����ȵ��׽���
            except:
                time.sleep(0.01)#û��ȡ��ʱ��ͣ0.01���ٻ�ȡ
                continue

            if data:#��ȡ���׽���ʱ
                total_data.append(data)
                bytes_remaining -= len(data)#ָ�����ȼ�ȥ��ͷ�����ĳ��Ⱥ���Ԥ������Ϊ0
                if bytes_remaining <= 0:#
                    for i in range(len(total_data)):#���׽��ִ����б����ݴ��ֽ�תΪ�ַ���
                        total_data[i] = total_data[i].decode()

                    if reply_length == 0:#Ϊ0ʱΪ��ͷ
                        header = ''.join(total_data)
                        reply_length = int(header)#��ͷ�����α�ʾ����ĳ���
                        bytes_remaining = reply_length#��ָ������ָ��Ϊ����ĳ���
                        total_data = []#����׽��ִ����б�
                    else:#��ʱΪ����
                        if self.discard_count > 0:#����Ҫ����ʱ
                            self.discard_count -= 1
                            return self.recv()#��ʱʱ���¼�����һ��

                        reply_json = ''.join(total_data)
                        return json.loads(reply_json)

        self.discard_count += 1#����ʱʱ����Ҫ�����ļ����׽��ּ�һ���Է�������
        raise RuntimeError('�ȴ���Ӧ��ʱ')

    def is_valid_reply(self, reply):
        """
        ��鷵����Ϣ�Ƿ����Ԥ�ڹ淶
        :param reply: Ҫ������Ϣ
        :return: True:����
                 False:������
        """
        if not reply:
            print('[error] ��Ч��')
            return False

        if not reply['success']:
            print('[error] {} ʧ��: {}'.format(reply['cmd'], reply['msg']))
            return

        return True

    def ping(self):
        cmd = {'cmd': 'ping'}

        reply = self.send(cmd)

        if self.is_valid_reply(reply):
            return True
        else:
            return False

class ExampleClient(ClientBase):
    PORT = 20201

    def echo(self, text):
        cmd = {'cmd': 'echo',
               'text': text}
        reply = self.send(cmd)
        if self.is_valid_reply(reply):
            return reply['result']
        else:
            return None

    def set_title(self, title):
        cmd = {'cmd': 'set_title',
               'title': title}

        reply = self.send(cmd)
        if self.is_valid_reply(reply):
            return reply['result']
        else:
            return None

    def sleep(self):
        cmd = {'cmd': 'sleep'}

        reply = self.send(cmd)
        if self.is_valid_reply(reply):
            return reply['result']
        else:
            return None


if __name__ == '__main__':
    client = ExampleClient()
    if client.connect():
        print('���ӳɹ�')

        print(client.ping())#�����׽����Ƿ��ܹ�pingͨ
        #print(client.echo('�ɹ�����'))
        #print(client.set_title(u'���Ǳ���'))
        print(client.sleep())#��Ϊ�ڻ�����Ĭ�������˵ȴ�����˻�Ӧʱ��Ϊ2�룬������˸÷����ȴ���6�룬���Իᱨ�����ȴ�ʱ��
        if client.disconnect():
            print('�Ͽ�����')
    else:
        print('����ʧ��')
