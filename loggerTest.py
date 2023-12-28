#coding=gbk
import logging
import sys


#https://docs.python.org/3/library/logging.html
class Logger(object):
    PROPAGATE_DEFAULT = True

    FORMAT_DEFAULT = '[%(name)s][%(levelname)s]文件%(filename)s第%(lineno)d行:%(message)s'
    LOGGER_NAME = 'aa'
    LEVEL_DEFAUIT = logging.DEBUG
    _logger_obj = None

    @classmethod
    def logger_obj(cls):
        if not cls._logger_obj:
            if cls.logger_exists():#检查日志管理器中是否已存在具有指定名称的记录器。避免创建重复的记录器
                cls._logger_obj = logging.getLogger(cls.LOGGER_NAME)
            else:
                cls._logger_obj = logging.getLogger(cls.LOGGER_NAME)
                cls._logger_obj.setLevel(cls.LEVEL_DEFAUIT)
                cls._logger_obj.propagate = cls.PROPAGATE_DEFAULT
                fmt = logging.Formatter(cls.FORMAT_DEFAULT)
                #以百分号开头，以类型字符结尾。姓名，信息级别，信息
                #其余类型如asctime：时间、filename：文件名、funcName：函数名、lineno：行数、module：模块、pathname：路径、threadName：线程名

                #创建一个流处理程序，将日志消息写入标准错误sys.stderr
                stream_handler = logging.StreamHandler(sys.stderr)#改为stdout可以在Maya中不打印前面的#号
                stream_handler.setFormatter(fmt)#将格式化程序fmt设置为流处理程序
                cls._logger_obj.addHandler(stream_handler)#将流处理程序添加到记录器

        return cls._logger_obj#号

    @classmethod
    def logger_exists(cls):
        """
        此方法检查日志管理器中是否已存在具有指定名称的记录器。loggerDict它通过检查记录器的名称是否在日志记录管理器属性的键中来实现此目的
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
    #当在Maya中运行logger时，创建的记录器会被视为Maya主记录器的子记录器，所以在Maya中直接运行时会重复记录
    Logger.set_propagate(False)#将propagate设置为false可以打断与主记录器的链接，默认为True

    Logger.error('打印一下')
