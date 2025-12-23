from loguru import logger


class PacketParser:
    """帧处理层：负责指令帧生成和数据帧解析"""
    
    # 帧格式定义
    START_BYTE = 0xAA
    END_BYTE = 0x55
    
    # 命令ID定义
    CMD_GET_TEMPERATURE = 0x01
    CMD_GET_CURRENT = 0x02
    CMD_GET_POWER = 0x03
    
    def __init__(self):
        pass
    
    def create_command_packet(self, command_id: int, data: bytes = b''):
        """生成指令帧
        
        帧格式：[起始字节][命令ID][数据长度][数据内容][校验和][结束字节]
        
        Args:
            command_id: 命令ID
            data: 命令数据
            
        Returns:
            bytes: 完整的指令帧
        """
        frame = bytearray()
        
        # 起始字节
        frame.append(self.START_BYTE)
        
        # 命令ID
        frame.append(command_id)
        
        # 数据长度
        data_len = len(data)
        frame.append(data_len & 0xFF)
        frame.append((data_len >> 8) & 0xFF)  # 支持16位长度
        
        # 数据内容
        frame.extend(data)
        
        # 校验和 (简单的异或校验)
        checksum = 0
        for byte in frame[1:]:  # 不包括起始字节
            checksum ^= byte
        frame.append(checksum)
        
        # 结束字节
        frame.append(self.END_BYTE)
        
        return bytes(frame)
    
    def parse_received_data(self, raw_data: bytes):
        """解析接收到的数据
        
        Args:
            raw_data: 原始数据
            
        Returns:
            dict: 解析后的帧数据，格式为 {'command_id': int, 'data': bytes}，如果没有完整帧返回None
        """
        if len(raw_data) < 6:  # 最小帧长度：起始+命令+长度低+长度高+校验+结束
            return None
        
        # 查找起始字节
        start_idx = raw_data.find(self.START_BYTE)
        if start_idx == -1:
            return None
        
        # 查找结束字节
        end_idx = raw_data.find(self.END_BYTE, start_idx + 1)
        if end_idx == -1:
            return None
        
        # 提取完整帧
        frame = raw_data[start_idx:end_idx + 1]
        
        # 验证帧长度
        if len(frame) < 6:
            return None
        
        # 验证校验和
        checksum = 0
        for byte in frame[1:-2]:  # 不包括起始字节和最后两个字节(校验和+结束字节)
            checksum ^= byte
        
        if checksum != frame[-2]:
            logger.error(f'Checksum mismatch. Calculated: {checksum:02X}, Received: {frame[-2]:02X}')
            return None
        
        # 解析帧内容
        command_id = frame[1]
        data_len = frame[2] | (frame[3] << 8)
        
        if len(frame) != 6 + data_len:  # 验证总长度
            logger.error(f'Frame length mismatch. Expected: {6 + data_len}, Actual: {len(frame)}')
            return None
        
        data = frame[4:-2]  # 数据部分
        
        return {
            'command_id': command_id,
            'data': data
        }
    
    def parse_temperature_data(self, data: bytes):
        """解析温度数据
        
        假设温度数据格式为：2字节小端，单位为0.1℃
        
        Args:
            data: 温度数据
            
        Returns:
            float: 温度值(℃)
        """
        if len(data) < 2:
            logger.error(f'Invalid temperature data length: {len(data)}')
            return None
        
        temperature_raw = int.from_bytes(data[:2], byteorder='little')
        temperature = temperature_raw * 0.1  # 转换为℃
        
        return temperature
    
    def parse_current_data(self, data: bytes):
        """解析电流数据
        
        假设电流数据格式为：4字节小端，单位为0.001A
        
        Args:
            data: 电流数据
            
        Returns:
            float: 电流值(A)
        """
        if len(data) < 4:
            logger.error(f'Invalid current data length: {len(data)}')
            return None
        
        current_raw = int.from_bytes(data[:4], byteorder='little')
        current = current_raw * 0.001  # 转换为A
        
        return current
    
    def parse_power_data(self, data: bytes):
        """解析功率数据
        
        假设功率数据格式为：4字节小端，单位为0.001W
        
        Args:
            data: 功率数据
            
        Returns:
            float: 功率值(W)
        """
        if len(data) < 4:
            logger.error(f'Invalid power data length: {len(data)}')
            return None
        
        power_raw = int.from_bytes(data[:4], byteorder='little')
        power = power_raw * 0.001  # 转换为W
        
        return power
