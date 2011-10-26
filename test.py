#! /usr/bin/env python2.7
# coding: utf-8

__all__ = ['TestSimpleMQ']

import unittest
from redis import Redis
from simplemq import SimpleMQ
from time import localtime

class Q(SimpleMQ):
    @classmethod
    def handler(cls, msg):
        if msg == 'exit':
            exit()

class TestSimpleMQ(unittest.TestCase):

    def setUp(self):
        self.r = Redis()
        self.tearDown()

    def tearDown(self):
        self.r.flushdb()

    def test_client(self):
        assert isinstance(SimpleMQ.client, Redis)

    def test_name(self):
        assert SimpleMQ.name() != ""

    def test_enqueue_and_dequeue(self):
        self.data = "hello moto"

        assert SimpleMQ.enqueue(self.data) is True

        assert self.r.exists(SimpleMQ.name())

        assert SimpleMQ.dequeue() == self.data

    def test_raise_when_enqueue_not_valid_data(self):
        self.set = {'a', 'b', 'c'}

        with self.assertRaises(TypeError):
            SimpleMQ.enqueue(self.set)

    def test_length(self):
        assert Q.length() == 0

        Q.enqueue('hi')
        assert Q.length() == 1

    def test_handler_and_worker(self):
        Q.enqueue('exit')

        with self.assertRaises(SystemExit):
            Q.worker()

    def test_worker_with_delay(self):
        Q.enqueue('exit')

        self.before = localtime().tm_sec
        self.delay = 1

        with self.assertRaises(SystemExit):
            Q.worker(delay=self.delay)

        # 放松时间要求，防止测试失败
        assert self.before + self.delay \
               <= localtime().tm_sec \
               <= self.before + self.delay+1
    
if __name__ == "__main__":
    unittest.main()
