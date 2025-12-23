from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer
from loguru import logger
from backend.communication.packet_parser import PacketParser
from backend.communication.communication_interface import CommunicationInterface


class DataAcquisition(QObject):
    """应用层：数据采集器，负责与板卡通信获取各类数据"""
    
    # 信号定义
    temperature_updated = pyqtSignal(float)
    current_updated = pyqtSignal(float)
    power_updated = pyqtSignal(float)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, communication_interface: CommunicationInterface):
        super().__init__()
        self._communication = communication_interface
        self._parser = PacketParser()
        self._timer = None
        self._is_running = False
        self._buffer = b''
    
    def connect(self):
        """建立连接"""
        try:
            self._communication.open()
            logger.info('Data acquisition connected')
        except Exception as e:
            logger.error(f'Failed to connect: {e}')
            self.error_occurred.emit(f'连接失败: {str(e)}')
            raise
    
    def disconnect(self):
        """断开连接"""
        try:
            if self._timer:
                self._timer.stop()
            self._communication.close()
            self._is_running = False
            logger.info('Data acquisition disconnected')
        except Exception as e:
            logger.error(f'Failed to disconnect: {e}')
            self.error_occurred.emit(f'断开连接失败: {str(e)}')
            raise
    
    def start_auto_acquisition(self, interval=1000):
        """开始自动采集
        
        Args:
            interval: 采集间隔(毫秒)
        """
        if not self._communication.is_open():
            logger.error('Cannot start acquisition: communication not open')
            self.error_occurred.emit('通信未建立，无法开始采集')
            return
        
        if self._timer is None:
            self._timer = QTimer()
            self._timer.timeout.connect(self._acquire_all_data)
        
        self._timer.start(interval)
        self._is_running = True
        logger.info(f'Started auto acquisition with interval {interval}ms')
    
    def stop_auto_acquisition(self):
        """停止自动采集"""
        if self._timer:
            self._timer.stop()
        self._is_running = False
        logger.info('Stopped auto acquisition')
    
    def get_temperature(self):
        """手动获取温度数据"""
        return self._get_data(PacketParser.CMD_GET_TEMPERATURE)
    
    def get_current(self):
        """手动获取电流数据"""
        return self._get_data(PacketParser.CMD_GET_CURRENT)
    
    def get_power(self):
        """手动获取功率数据"""
        return self._get_data(PacketParser.CMD_GET_POWER)
    
    def _get_data(self, command_id: int):
        """发送命令并获取数据
        
        Args:
            command_id: 命令ID
            
        Returns:
            float: 获取的数据值
        """
        if not self._communication.is_open():
            logger.error('Cannot get data: communication not open')
            self.error_occurred.emit('通信未建立，无法获取数据')
            return None
        
        try:
            # 生成命令帧
            packet = self._parser.create_command_packet(command_id)
            
            # 发送命令
            self._communication.send(packet)
            
            # 接收响应
            response = self._communication.receive(timeout=2.0)
            
            if not response:
                logger.error('No response received')
                self.error_occurred.emit('无响应数据')
                return None
            
            # 解析响应
            parsed_frame = self._parser.parse_received_data(response)
            
            if not parsed_frame or parsed_frame['command_id'] != command_id:
                logger.error('Invalid response received')
                self.error_occurred.emit('无效的响应数据')
                return None
            
            # 根据命令ID解析具体数据
            if command_id == PacketParser.CMD_GET_TEMPERATURE:
                return self._parser.parse_temperature_data(parsed_frame['data'])
            elif command_id == PacketParser.CMD_GET_CURRENT:
                return self._parser.parse_current_data(parsed_frame['data'])
            elif command_id == PacketParser.CMD_GET_POWER:
                return self._parser.parse_power_data(parsed_frame['data'])
            else:
                logger.error(f'Unsupported command: {command_id}')
                self.error_occurred.emit(f'不支持的命令: {command_id}')
                return None
                
        except Exception as e:
            logger.error(f'Error getting data: {e}')
            self.error_occurred.emit(f'获取数据失败: {str(e)}')
            return None
    
    def _acquire_all_data(self):
        """采集所有数据"""
        # 获取温度
        temperature = self.get_temperature()
        if temperature is not None:
            self.temperature_updated.emit(temperature)
        
        # 获取电流
        current = self.get_current()
        if current is not None:
            self.current_updated.emit(current)
        
        # 获取功率
        power = self.get_power()
        if power is not None:
            self.power_updated.emit(power)


class DataAcquisitionWorker(QThread):
    """数据采集工作线程，用于异步处理数据采集"""
    
    temperature_updated = pyqtSignal(float)
    current_updated = pyqtSignal(float)
    power_updated = pyqtSignal(float)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, communication_interface: CommunicationInterface):
        super().__init__()
        self._data_acquisition = DataAcquisition(communication_interface)
        self._data_acquisition.temperature_updated.connect(self.temperature_updated)
        self._data_acquisition.current_updated.connect(self.current_updated)
        self._data_acquisition.power_updated.connect(self.power_updated)
        self._data_acquisition.error_occurred.connect(self.error_occurred)
    
    def run(self):
        """线程运行函数"""
        try:
            self._data_acquisition.connect()
            self._data_acquisition.start_auto_acquisition()
            self.exec_()  # 启动事件循环
        except Exception as e:
            logger.error(f'Data acquisition thread error: {e}')
            self.error_occurred.emit(f'线程错误: {str(e)}')
    
    def stop(self):
        """停止采集线程"""
        try:
            self._data_acquisition.stop_auto_acquisition()
            self._data_acquisition.disconnect()
            self.quit()
            self.wait()
        except Exception as e:
            logger.error(f'Error stopping data acquisition thread: {e}')
    
    def get_temperature(self):
        """获取温度数据"""
        return self._data_acquisition.get_temperature()
    
    def get_current(self):
        """获取电流数据"""
        return self._data_acquisition.get_current()
    
    def get_power(self):
        """获取功率数据"""
        return self._data_acquisition.get_power()
