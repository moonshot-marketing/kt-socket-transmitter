#
# Bi project
# Socket Transmitter Class
#
# @created 2017-03-21
# @last modified 2017-03-21
# @copyright moonshot marketing
# @author Itay Zagron
#


import socket
import json
from abc import ABCMeta, abstractmethod
import logging

SUCCESS = 'MSG_RECEIVED'
END_MESSAGE = '\x04'


class SocketTransmitter(object):

    __metaclass__ = ABCMeta

    def __init__(self, tcp_ip, tcp_port, logger_name, buffer_size=1024):

        # init logger
        self.logger = logging.getLogger(logger_name)

        self.logger.info('\n\n')
        self.logger.info('New Socket Transmitter Open With ip: %s and port %d' % (tcp_ip, tcp_port))
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.buffer_size = buffer_size

        self.socket = None

    def __del__(self):
        pass

    @abstractmethod
    def build_message(self, **kwargs):
        pass

    def execute(self, message):

        # initialize new socket
        self._initialize()
        self.logger.info('socket initialize successfully.')

        # connect to pair
        self.logger.info('current message: %s' % message)
        if self._connect():
            self.logger.info('socket connect to server successfully.')
            self._send_message(message)
            if self._receive_message() == SUCCESS:
                self.logger.info('socket send message successfully.')
            else:
                self.logger.error('message sent but response is empty.')

            self._disconnect()

        else:
            self.logger.error('socket isn\'t connected, message not sent.')

    def _connect(self):
        try:
            self.socket.connect((self.tcp_ip, self.tcp_port))
            return True
        except socket.error, exc:
            self.logger.error('socket connect error: %s' % repr(exc))
            return False

    def _initialize(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, exc:
            self.logger.error('socket initialize error: %s' % exc.message)

    def _disconnect(self):
        try:
            self.socket.close()
            self.logger.info('socket disconnect successfully.')
        except socket.error, exc:
            self.logger.error('socket disconnect error: %s' % exc.message)

    def _send_message(self, message):
        try:
            f = self.socket.makefile()
            f.write(message + END_MESSAGE)
            f.flush()

        except socket.error, exc:
            self.logger.error('message send error: %s' % exc.message)

    def _receive_message(self):
        try:
            return self.socket.recv(self.buffer_size)
        except socket.error, exc:
            self.logger.error('response receive error: %s' % exc.message)

__version__ = "1.0.0"
__all__ = ['SocketTransmitter', '__version__', 'json']