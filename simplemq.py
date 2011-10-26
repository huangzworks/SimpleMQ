# coding: utf-8

__all__ = ['SimpleMQ']

__metaclass__ = type

from json import dumps as encode, loads as decode
from redis import Redis
from time import sleep

DATABASE_PREFIX_TAG = 'SimpleMQ::'

class SimpleMQ:
    
    client = Redis() 

    @classmethod
    def name(cls):
        """ 返回队列的名字。

        Args:
            cls
        Time:
            O(1)
        Return:
            name
        Raises:
            none
        """
        return DATABASE_PREFIX_TAG + cls.__name__

    @classmethod
    def enqueue(cls, msg):
        """ 将消息入队。
        
        Args:
            cls
            msg: 消息内容，可以是任何能被转作 JSON 格式的数据。
        Time:
            O(1)
        Return:
            bool: 入队成功返回 True ，否则返回 False 。
        Raises:
            TypeError: 试图将不能转为 JSON 格式的数据传入时抛出。
        """
        encoded_msg = encode(msg)
        status = cls.client.lpush(cls.name(), encoded_msg)
        return bool(status)

    @classmethod
    def dequeue(cls):
        """ 将消息出队，如果队列为空，则阻塞直到有消息可弹出为止。
        
        Args:
            cls
        Time:
            O(1)
        Return:
            msg
        Raises:
            none
        """
        queue_name, encoded_msg = cls.client.brpop(cls.name())
        msg = decode(encoded_msg)
        return msg

    @classmethod
    def handler(cls, msg):
        """ 消息处理器，用户通过覆盖这个类方法来提供功能。 
        
        Args:
            cls
            msg
        Time:
            undefined
        Return:
            undefined
        Raises:
            NotImplementedError: 方法未被覆盖时抛出。
        """
        # TODO: 在 Python3 中可以用 abstractclassmethod 来实现
        raise NotImplementedError

    @classmethod
    def worker(cls, delay=0):
        """ 处理器loop。 
        
        Args:
            cls
            delay: 处理消息的间隔，默认为0。
        Time:
            O(N)
        Return:
            None
        Raises:
            none
        """
        while sleep(delay) is None:
            msg = cls.dequeue()
            cls.handler(msg)

    @classmethod
    def length(cls):
        """ 返回队列中消息的数量。

        Args:
            cls
        Time:
            O(1)
        Return:
            length
        Raises:
            none
        """
        return cls.client.llen(cls.name())


