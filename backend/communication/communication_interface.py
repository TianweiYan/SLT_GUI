from abc import ABC, abstractmethod


class CommunicationInterface(ABC):
    """物理层通信接口抽象类"""
    
    @abstractmethod
    def open(self):
        """打开通信通道"""
        pass
    
    @abstractmethod
    def close(self):
        """关闭通信通道"""
        pass
    
    @abstractmethod
    def send(self, data: bytes):
        """发送数据
        
        Args:
            data: 要发送的字节数据
        """
        pass
    
    @abstractmethod
    def receive(self, timeout=None):
        """接收数据
        
        Args:
            timeout: 超时时间，单位秒
            
        Returns:
            bytes: 接收到的字节数据
        """
        pass
    
    @abstractmethod
    def is_open(self):
        """检查通信通道是否打开
        
        Returns:
            bool: 通信通道是否打开
        """
        pass
