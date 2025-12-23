import socket
from loguru import logger
from backend.communication.communication_interface import CommunicationInterface


class NetworkPort(CommunicationInterface):
    """网口通信实现"""
    
    def __init__(self, host, port, timeout=1):
        self.host = host
        self.port = port
        self.timeout = timeout
        self._socket = None
    
    def open(self):
        """打开网口连接"""
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(self.timeout)
            self._socket.connect((self.host, self.port))
            logger.info(f'Connected to network {self.host}:{self.port}')
        except Exception as e:
            logger.error(f'Failed to connect to {self.host}:{self.port}: {e}')
            raise
    
    def close(self):
        """关闭网口连接"""
        if self._socket:
            self._socket.close()
            logger.info(f'Network connection to {self.host}:{self.port} closed')
    
    def send(self, data: bytes):
        """发送数据"""
        if self._socket:
            try:
                self._socket.sendall(data)
                logger.debug(f'Sent {len(data)} bytes over network: {data.hex()}')
            except Exception as e:
                logger.error(f'Failed to send data over network: {e}')
                raise
        else:
            logger.error('Network connection not established')
            raise ConnectionError('Network connection not established')
    
    def receive(self, timeout=None):
        """接收数据"""
        if self._socket:
            try:
                original_timeout = self._socket.gettimeout()
                if timeout is not None:
                    self._socket.settimeout(timeout)
                
                data = self._socket.recv(1024)  # 最大读取1024字节
                
                if timeout is not None:
                    self._socket.settimeout(original_timeout)
                
                if data:
                    logger.debug(f'Received {len(data)} bytes over network: {data.hex()}')
                return data
            except Exception as e:
                logger.error(f'Failed to receive data over network: {e}')
                raise
        else:
            logger.error('Network connection not established')
            raise ConnectionError('Network connection not established')
    
    def is_open(self):
        """检查连接是否打开"""
        # 简单检查，实际应用中可能需要更复杂的状态管理
        return self._socket is not None
