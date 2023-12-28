#coding=gbk
import logging
import sys


#https://docs.python.org/3/library/logging.html
class Logger(object):
    PROPAGATE_DEFAULT = True

    FORMAT_DEFAULT = '[%(name)s][%(levelname)s]�ļ�%(filename)s��%(lineno)d��:%(message)s'
    LOGGER_NAME = 'aa'
    LEVEL_DEFAUIT = logging.DEBUG
    _logger_obj = None

    @classmethod
    def logger_obj(cls):
        if not cls._logger_obj:
            if cls.logger_exists():#�����־���������Ƿ��Ѵ��ھ���ָ�����Ƶļ�¼�������ⴴ���ظ��ļ�¼��
                cls._logger_obj = logging.getLogger(cls.LOGGER_NAME)
            else:
                cls._logger_obj = logging.getLogger(cls.LOGGER_NAME)
                cls._logger_obj.setLevel(cls.LEVEL_DEFAUIT)
                cls._logger_obj.propagate = cls.PROPAGATE_DEFAULT
                fmt = logging.Formatter(cls.FORMAT_DEFAULT)
                #�԰ٷֺſ�ͷ���������ַ���β����������Ϣ������Ϣ
                #����������asctime��ʱ�䡢filename���ļ�����funcName����������lineno��������module��ģ�顢pathname��·����threadName���߳���

                #����һ����������򣬽���־��Ϣд���׼����sys.stderr
                stream_handler = logging.StreamHandler(sys.stderr)#��Ϊstdout������Maya�в���ӡǰ���#��
                stream_handler.setFormatter(fmt)#����ʽ������fmt����Ϊ���������
                cls._logger_obj.addHandler(stream_handler)#�������������ӵ���¼��

        return cls._logger_obj#��

    @classmethod
    def logger_exists(cls):
        """
        �˷��������־���������Ƿ��Ѵ��ھ���ָ�����Ƶļ�¼����loggerDict��ͨ������¼���������Ƿ�����־��¼���������Եļ�����ʵ�ִ�Ŀ��
        :return:
        """
        return cls.LOGGER_NAME in logging.Logger.manager.loggerDict.keys()

    @classmethod
    def debug(cls, msg, *args, **kwargs):
        lg = cls.logger_obj()
        lg.debug(msg, *args, ** kwargs)

    @classmethod
    def info(cls, msg, *args, **kwargs):
        lg = cls.logger_obj()
        lg.info(msg, *args, **kwargs)

    @classmethod
    def warning(cls, msg, *args, **kwargs):
        lg = cls.logger_obj()
        lg.warning(msg, *args, **kwargs)

    @classmethod
    def error(cls, msg, *args, **kwargs):
        lg = cls.logger_obj()
        lg.error(msg, *args, **kwargs)

    @classmethod
    def critical(cls, msg, *args, **kwargs):
        lg = cls.logger_obj()
        lg.critical(msg, *args, **kwargs)

    @classmethod
    def log(cls, level, msg, *args, **kwargs):
        lg = cls.logger_obj()
        lg.log(level, msg, *args, **kwargs)

    @classmethod
    def exception(cls, msg, *args, **kwargs):
        lg = cls.logger_obj()
        lg.exception(msg, *args, **kwargs)

    @classmethod
    def setLevel(cls, level):
        lg = cls.logger_obj()
        lg.setLevel(level)

    @classmethod
    def set_propagate(cls, propagate):
        lg = cls.logger_obj()
        lg.propagate = propagate

    @classmethod
    def write_to_file(cls, path, level=logging.WARNING):
        file_handler = logging.FileHandler(path)
        file_handler.setLevel(level)

        fmt = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
        file_handler.setFormatter(fmt)

        lg = cls.logger_obj()
        lg.addHandler(file_handler)

    def __init__(self):
        pass

if __name__ == "__main__":
    #����Maya������loggerʱ�������ļ�¼���ᱻ��ΪMaya����¼�����Ӽ�¼����������Maya��ֱ������ʱ���ظ���¼
    Logger.set_propagate(False)#��propagate����Ϊfalse���Դ��������¼�������ӣ�Ĭ��ΪTrue

    Logger.error('��ӡһ��')
