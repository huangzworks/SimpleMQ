关于 SimpleMQ
********************

SimpleMQ 是一个简单易用的消息队列(MQ,message queue)库，使用 Python2 写成，以 Reids 作为后端。

SimpleMQ 的口号是：“messaging that just work easier！”。


使用方法
===========

1. 用新类继承 ``SimpleMQ`` 类，并重载 ``handler`` 类方法，其中 ``handler`` 负责处理消息；
   如果有需要的话，你也可以指定 Redis 使用的客户端及其参数。

::

    from redis import Redis
    from time import ctime
    from simplemq import SimpleMQ
    
    class HelloWorldMQ(SimpleMQ):
    
        client = Redis(db=3)    # 指定 redis 客户端
    
        @classmethod
        def handler(cls, msg):
            print("Time: {0}".format(ctime()))
    
            if msg == "hello world":
                print(msg)
            else:
                print("i don't know what you say...")


2. 使用 ``enqueue`` 类方法将消息入队， ``worker`` 类方法接受一个参数(\ ``delay``\ )，用来指定处理消息的时间间隔。

::

    >>> from t import HelloWorldMQ
    >>> HelloWorldMQ.enqueue('hi')
    True
    >>> HelloWorldMQ.enqueue('morning')
    True
    >>> HelloWorldMQ.enqueue('hello world')
    True
    >>> HelloWorldMQ.worker(5)  # 每5秒处理一次消息
    Time: Wed Oct 26 14:13:28 2011
    'hi'??? i don't know what you say...
    Time: Wed Oct 26 14:13:33 2011
    'morning'??? i don't know what you say...
    Time: Wed Oct 26 14:13:38 2011
    hello world


3. 没有步骤三，耶！


API手册
=========

SimpleMQ.client
-----------------

接受一个 ``redis-py.Redis`` 的实例，作为MQ的客户端，默认为： ``client = Redis()`` 。

你可以在派生新类的时候将配置硬写进类定义里:

::

    class Q(SimpleMQ):
        client = Redis(db=3)
        # ...

也可以在解释器中动态改变客户端(反正就是赋值而已嘛！)

::
    
    # ...
    Q.client = Reids(db=5)
    # ...

SimpleMQ.name(cls)
----------------------

返回队列的名字。
队列名字全部以 ``'SimpleMQ::QueueClassName'`` 格式的Key名保存在 Redis 当中。

SimpleMQ.enqueue(cls, msg)
------------------------------

将 ``msg`` 保存到队列当中，接受所有能转换成 JSON 格式的数据。
如果 ``msg`` 保存成功，返回 ``True`` 。

SimpleMQ 以 FIFO 的方式入队和出队消息。

SimpleMQ.dequeue(cls)
----------------------

从队列中取出消息并返回。
如果队列中没有任何消息(队列为空)，则阻塞(block)直到有消息可返回为止。

如果自带的 handler + worker 的组合不能满足你的需求，你还可以用 ``dequeue`` 构造你自己的 worker：

::

    while True:
        msg = SimpleMQ.dequeue()
        # ...

SimpleMQ.handler(cls, msg)
------------------------------

你需要通过重载 ``handler`` 类方法来为默认的 ``worker`` 提供消息处理功能。

::

    class Q(SimpleMQ):
        @classmethod
        def handler(cls, msg):
            # ... 

请记住 ``handler`` 是一个类方法，它要用 ``@classmethod`` 装饰，并且需要 ``cls`` 和 ``msg`` 两个参数。

并且，SimpleMQ 将最大的权力和义务都留给了你 —— SimpleMQ 只提供了最基本的消息的入队和出队机制、以及 worker 的规定时间间隔运行，除此之外，它没有任何功能，一切都要靠你自己在 ``handler`` 方法中自力更生！

SimpleMQ.worker(cls, delay=0)
--------------------------------

``worker`` 函数接受一个参数 ``delay`` ，用来指定处理消息的间隔。
``delay`` 默认为 ``0`` ，既不作任何停顿。

SimpleMQ.length(cls)
---------------------

返回当前队列里等待处理的消息数量。


注意
=====

SimpleMQ 的内部实现是不安全队列，也就是说，如果处理消息的客户端失败的话(比如，handler 方法在运行过程中被强制退出)，消息就会丢失并得不到处理，因此，你应该\ *仅*\ 将 SimpleMQ 用于一些可丢失的任务当中。


需求
======

| Python 2.7
| redis-py 2.4.7
| Redis 2.4


安装
======

$ sudo pip2 install SimpleMQ


测试
=====

$ cd /SimpleMQ
$ ./test.py


许可
=====

你可以在免费且自由的情况下，下载、使用、修改本软件，如果你需要其他许可，请联系作者。


联系方式
========

twitter: @huangz1990
gmail: huangz1990
豆瓣: http://www.douban.com/people/i_m_huangz/
