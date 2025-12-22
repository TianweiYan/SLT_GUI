import serial
from loguru import logger

class SerialPort:
    def __init__(self, port, baud=115200, timeout=1):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self._ser = None

    def open(self):
        self._ser = serial.Serial(self.port, self.baud, timeout=self.timeout)
        logger.info(f'Opened serial {self.port}@{self.baud}')

    def close(self):
        if self._ser and self._ser.is_open:
            self._ser.close()
            logger.info('Serial closed')

    def send(self, data: bytes):
        if self._ser and self._ser.is_open:
            self._ser.write(data)
