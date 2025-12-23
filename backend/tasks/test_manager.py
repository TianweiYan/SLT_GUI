from backend.communication.data_acquisition import DataAcquisitionWorker
from backend.communication.serial_port import SerialPort
from backend.communication.network_port import NetworkPort
from backend.logger.logger import logger
from backend.config.config_loader import config_loader
import subprocess
import threading
import time

class TestManager:
    """测试管理器，负责处理测试逻辑"""
    
    def __init__(self):
        self.data_worker = None
        self.test_running = False
        self.test_thread = None
        
        # 测试结果数据
        self.test_results = {
            'start_time': None,
            'end_time': None,
            'ping_result': None,
            'commands_sent': 0,
            'data_received': 0,
            'errors': []
        }
    
    def start_test(self, on_status_update, on_error, on_test_complete):
        """开始测试
        
        Args:
            on_status_update: 状态更新回调函数
            on_error: 错误回调函数
            on_test_complete: 测试完成回调函数
        """
        if self.test_running:
            return
            
        self.test_running = True
        self.test_results = {
            'start_time': time.time(),
            'end_time': None,
            'ping_result': None,
            'commands_sent': 0,
            'data_received': 0,
            'errors': []
        }
        
        # 启动测试线程
        self.test_thread = threading.Thread(
            target=self._run_test,
            args=(on_status_update, on_error, on_test_complete)
        )
        self.test_thread.daemon = True
        self.test_thread.start()
    
    def stop_test(self):
        """停止测试"""
        self.test_running = False
        
        if self.data_worker:
            self.data_worker.stop()
            self.data_worker = None
    
    def _run_test(self, on_status_update, on_error, on_test_complete):
        """运行测试流程"""
        try:
            # 第一步：建立通信连接
            on_status_update("正在建立通信连接...")
            self._establish_connection()
            
            # 第二步：网口通信时进行ping测试
            comm_type = config_loader.get('communication.type')
            if comm_type == 'network':
                on_status_update("正在进行网络连接测试...")
                ip = config_loader.get('communication.network.ip')
                ping_count = config_loader.get('test.ping_count', 4)
                
                if self._ping_device(ip, ping_count):
                    self.test_results['ping_result'] = True
                    on_status_update("网络连接测试成功")
                else:
                    self.test_results['ping_result'] = False
                    on_status_update("网络连接测试失败")
                    raise Exception(f"Ping {ip} 失败，无法建立连接")
            
            # 第三步：发送测试指令
            on_status_update("开始发送测试指令...")
            self._send_test_commands()
            
            # 第四步：结束测试
            on_status_update("测试完成")
            
        except Exception as e:
            logger.error(f"测试过程中发生错误: {e}")
            on_error(f"测试失败: {str(e)}")
            self.test_results['errors'].append(str(e))
        finally:
            # 清理资源
            self._cleanup()
            
            # 记录结束时间
            self.test_results['end_time'] = time.time()
            
            # 通知测试完成
            on_test_complete(self.test_results)
    
    def _establish_connection(self):
        """建立通信连接"""
        # 从配置文件获取通信设置
        comm_type = config_loader.get('communication.type')
        
        if comm_type == 'serial':
            # 使用RS422串口
            serial_port = config_loader.get('communication.serial.port')
            baud_rate = config_loader.get('communication.serial.baud_rate')
            comm_interface = SerialPort(serial_port, baud=baud_rate)
            logger.info(f"准备连接RS422串口: {serial_port}@{baud_rate}")
        else:
            # 使用网口
            ip = config_loader.get('communication.network.ip')
            port = config_loader.get('communication.network.port')
            comm_interface = NetworkPort(ip, port)
            logger.info(f"准备连接网口: {ip}:{port}")
        
        # 创建并启动数据采集线程
        self.data_worker = DataAcquisitionWorker(comm_interface)
        # 可以在这里连接数据更新信号
        # self.data_worker.temperature_updated.connect(...)        
        self.data_worker.start()
    
    def _ping_device(self, ip, count=4):
        """ping设备
        
        Args:
            ip: 设备IP地址
            count: ping次数
            
        Returns:
            bool: ping是否成功
        """
        try:
            # Windows系统ping命令
            result = subprocess.run(
                ['ping', '-n', str(count), ip],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10
            )
            
            logger.info(f"Ping结果: {result.stdout}")
            
            # 检查ping结果
            if result.returncode == 0 and "TTL=" in result.stdout:
                # 统计成功次数
                success_count = result.stdout.count("TTL=")
                logger.info(f"Ping {ip} 成功 {success_count}/{count} 次")
                return success_count >= count // 2  # 至少一半成功
            
            return False
            
        except Exception as e:
            logger.error(f"Ping {ip} 失败: {e}")
            return False
    
    def _send_test_commands(self):
        """发送测试指令"""
        try:
            # 这里实现发送测试指令的逻辑
            # 示例：发送10条测试指令
            command_count = 10
            for i in range(command_count):
                if not self.test_running:
                    break
                    
                # 发送测试指令
                logger.info(f"发送测试指令 {i+1}/{command_count}")
                self.test_results['commands_sent'] += 1
                
                # 模拟发送延迟
                time.sleep(config_loader.get('test.command_interval', 0.5))
                
            logger.info("测试指令发送完成")
            
        except Exception as e:
            logger.error(f"发送测试指令失败: {e}")
            raise
    
    def _cleanup(self):
        """清理资源"""
        self.test_running = False
        
        if self.data_worker:
            self.data_worker.stop()
            self.data_worker = None
    
    def get_test_results(self):
        """获取测试结果"""
        return self.test_results
