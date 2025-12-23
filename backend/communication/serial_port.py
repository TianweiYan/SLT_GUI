import serial
from loguru import logger
from backend.communication.communication_interface import CommunicationInterface


class SerialPort(CommunicationInterface):
    """RS422串口通信实现"""
    
    def __init__(self, port, baud=115200, timeout=1):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self._ser = None

    def open(self):
        """打开串口"""
        try:
            self._ser = serial.Serial(self.port, self.baud, timeout=self.timeout)
            logger.info(f'Opened serial port {self.port}@{self.baud}')
        except Exception as e:
            logger.error(f'Failed to open serial port {self.port}: {e}')
            raise

    def close(self):
        """关闭串口"""
        if self._ser and self._ser.is_open:
            self._ser.close()
            logger.info(f'Serial port {self.port} closed')

    def send(self, data: bytes):
        """发送数据"""
        if self._ser and self._ser.is_open:
            try:
                self._ser.write(data)
                logger.debug(f'Sent {len(data)} bytes: {data.hex()}')
            except Exception as e:
                logger.error(f'Failed to send data: {e}')
                raise
        else:
            logger.error('Serial port not open')
            raise ConnectionError('Serial port not open')
    
    def receive(self, timeout=None):
        """接收数据"""
        if self._ser and self._ser.is_open:
            try:
                original_timeout = self._ser.timeout
                if timeout is not None:
                    self._ser.timeout = timeout
                
                data = self._ser.read(1024)  # 最大读取1024字节
                
                if timeout is not None:
                    self._ser.timeout = original_timeout
                
                if data:
                    logger.debug(f'Received {len(data)} bytes: {data.hex()}')
                return data
            except Exception as e:
                logger.error(f'Failed to receive data: {e}')
                raise
        else:
            logger.error('Serial port not open')
            raise ConnectionError('Serial port not open')
    
    def is_open(self):
        """检查串口是否打开"""
        return self._ser and self._ser.is_open
