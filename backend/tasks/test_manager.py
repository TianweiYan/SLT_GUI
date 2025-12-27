from backend.communication.data_acquisition import DataAcquisitionWorker
from backend.communication.serial_port import SerialPort
from backend.communication.network_port import NetworkPort
from backend.communication.packet_parser import PacketParser
from backend.logger.logger import logger
from backend.config.config_loader import config_loader
from backend.tasks.test_command_manager import TestCommandManager
from backend.tasks.command_sender import CommandSender
from backend.tasks.data_processor import DataProcessor
import subprocess
import threading
import time

class TestManager:
    """测试管理器，负责处理测试逻辑"""
    
    def __init__(self):
        self.data_worker = None
        self.test_running = False
        self.test_thread = None
        
        # 测试指令管理器
        self.command_manager = TestCommandManager()
        
        # 指令发送器和数据处理器
        self.command_sender = None
        self.data_processor = None
        
        # UI更新回调
        self.on_status_update = None
        self.on_error = None
        self.on_test_complete = None
        self.on_command_updated = None
        self.on_data_processed = None
        
        # 测试结果数据
        self.test_results = {
            'start_time': None,
            'end_time': None,
            'ping_result': None,
            'commands_sent': 0,
            'data_received': 0,
            'errors': [],
            'command_results': []
        }
        
        # 当前等待响应的指令信息
        self.current_expected_response = None
    
    def start_test(self, on_status_update, on_error, on_test_complete, on_command_updated=None, on_data_processed=None):
        """开始测试
        
        Args:
            on_status_update: 状态更新回调函数
            on_error: 错误回调函数
            on_test_complete: 测试完成回调函数
            on_command_updated: 指令更新回调函数（用于实时更新UI）
            on_data_processed: 数据处理完成回调函数（用于实时更新UI）
        """
        if self.test_running:
            return
            
        self.test_running = True
        self.on_status_update = on_status_update
        self.on_error = on_error
        self.on_test_complete = on_test_complete
        self.on_command_updated = on_command_updated
        self.on_data_processed = on_data_processed
        
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
            
            # 第三步：初始化指令发送器和数据处理器
            on_status_update("初始化指令发送器和数据处理器...")
            
            # 获取通信接口
            comm_interface = self.data_worker._data_acquisition._communication
            
            # 初始化指令发送器
            self.command_sender = CommandSender(comm_interface)
            self.command_sender.start()
            
            # 初始化数据处理器
            self.data_processor = DataProcessor()
            self.data_processor.start()
            
            # 启动响应处理线程
            threading.Thread(target=self._process_responses, daemon=True).start()
            
            # 启动结果处理线程
            threading.Thread(target=self._process_results, daemon=True).start()
            
            # 第四步：发送测试指令
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
        
        try:
            if comm_type == 'serial':
                # 使用RS422串口
                serial_port = config_loader.get('communication.serial.port')
                baud_rate = config_loader.get('communication.serial.baud_rate')
                
                # 验证必要的配置参数
                if not serial_port:
                    raise ValueError("未配置串口端口")
                if not baud_rate:
                    raise ValueError("未配置串口波特率")
                
                comm_interface = SerialPort(serial_port, baud=baud_rate)
                logger.info(f"准备连接RS422串口: {serial_port}@{baud_rate}")
            else:
                # 使用网口
                ip = config_loader.get('communication.network.ip')
                port = config_loader.get('communication.network.port')
                
                # 验证必要的配置参数
                if not ip:
                    raise ValueError("未配置网络IP地址")
                if not port:
                    raise ValueError("未配置网络端口")
                
                comm_interface = NetworkPort(ip, port)
                logger.info(f"准备连接网口: {ip}:{port}")
            
            # 创建并启动数据采集线程
            self.data_worker = DataAcquisitionWorker(comm_interface)
            # 可以在这里连接数据更新信号
            # self.data_worker.temperature_updated.connect(...)
            self.data_worker.start()
            
        except ValueError as e:
            logger.error(f"通信配置错误: {e}")
            # 确保资源被清理
            if hasattr(self, 'data_worker') and self.data_worker:
                self.data_worker.stop()
                self.data_worker = None
            raise
        except ConnectionError as e:
            logger.error(f"通信连接错误: {e}")
            # 确保资源被清理
            if hasattr(self, 'data_worker') and self.data_worker:
                self.data_worker.stop()
                self.data_worker = None
            raise
        except Exception as e:
            logger.error(f"建立通信连接失败: {e}")
            # 确保资源被清理
            if hasattr(self, 'data_worker') and self.data_worker:
                self.data_worker.stop()
                self.data_worker = None
            raise
    
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
            # 获取所有测试指令
            commands = self.command_manager.get_commands()
            command_count = len(commands)
            
            if command_count == 0:
                logger.warning("没有加载到测试指令")
                return
            
            logger.info(f"开始发送 {command_count} 条测试指令")
            
            # 将所有指令加入发送队列
            for i, command in enumerate(commands):
                if not self.test_running:
                    logger.info("测试已停止，中断指令发送")
                    break
                    
                # 添加到指令发送队列
                self.command_sender.send_command(command)
                
                # 更新指令状态
                self.command_manager.update_command_status(i, 'sending')
                
                # 通知UI更新
                if self.on_command_updated:
                    self.on_command_updated(command, 'sending')
                
                logger.info(f"指令已加入队列 {i+1}/{command_count}: {command['description']}")
            
            logger.info("所有测试指令已加入发送队列")
            
        except Exception as e:
            logger.error(f"发送测试指令失败: {e}")
            raise
    
    def _receive_response(self, timeout=2.0):
        """接收响应数据
        
        Args:
            timeout: 超时时间(秒)
            
        Returns:
            bytes: 响应数据，如果超时或出错则返回None
        """
        try:
            if not hasattr(self.data_worker, '_data_acquisition') or not hasattr(self.data_worker._data_acquisition, '_communication'):
                logger.error("无法接收响应: 通信接口不可用")
                return None
            
            comm_interface = self.data_worker._data_acquisition._communication
            
            # 检查通信接口是否已打开
            if not comm_interface.is_open():
                logger.error("无法接收响应: 通信接口未打开")
                return None
            
            # 尝试接收响应
            response = comm_interface.receive(timeout=timeout)
            
            if response is None or len(response) == 0:
                logger.warning(f"接收响应超时 ({timeout}秒)")
                return None
            
            return response
        except ConnectionError as e:
            logger.error(f"接收响应失败: 连接错误 - {e}")
            # 连接错误可能导致通信中断，需要重新建立连接
            if self.data_worker:
                self.data_worker.stop()
                self.data_worker = None
            return None
        except Exception as e:
            logger.error(f"接收响应失败: 未知错误 - {e}")
            return None
    
    def _process_response(self, response):
        """处理响应数据
        
        Args:
            response: 响应数据
            
        Returns:
            bool: 响应是否与当前期望的指令匹配
        """
        try:
            # 这里可以根据实际需求处理响应数据
            logger.info(f"收到响应数据: {response.hex()}")
            
            # 解析用户特定格式的测试指令响应
            # 格式参考：AA 55 55 AA 88 88 00 10 00 00 00 00 CF 10 00 01 00 00 0D EE
            if len(response) >= 12:
                # 检查响应头
                if response[:4] == b'\xAA\x55\x55\xAA':
                    logger.info("收到有效响应帧")
                    
                    # 解析帧结构
                    header = response[4:6]          # 帧头 88 88
                    length = int.from_bytes(response[6:8], byteorder='big')  # 数据长度
                    frame_id = response[8:12]       # 帧ID
                    
                    logger.info(f"帧头: {header.hex()}, 数据长度: {length}, 帧ID: {frame_id.hex()}")
                    
                    # 解析数据部分
                    if len(response) >= 12 + length:
                        data = response[12:12+length]
                        logger.info(f"响应数据: {data.hex()}")
                        
                        # 解析状态码
                        response_command_id = None
                        if len(data) >= 4:
                            # 假设命令ID在数据部分的2-3字节位置
                            response_command_id = data[2:4]
                            logger.info(f"命令码: {response_command_id.hex()}")
                            
                            # 解析状态码
                            status_code = data[:2] if len(data) >= 2 else b'0000'
                            logger.info(f"状态码: {status_code.hex()}")
                            
                            # 检查状态
                            if status_code == b'0000':
                                logger.info("命令执行成功")
                            else:
                                logger.warning(f"命令执行状态: {status_code.hex()} (可能失败)")
                    
                    # 验证响应是否与当前期望的指令匹配
                    if self.current_expected_response and response_command_id:
                        if self.current_expected_response['command_id'] == response_command_id:
                            logger.info(f"响应验证成功：指令 {self.current_expected_response['description']} 与响应匹配")
                            return True
                        else:
                            logger.warning(f"响应验证失败：指令 {self.current_expected_response['description']} 的命令ID {self.current_expected_response['command_id'].hex()} 与响应命令ID {response_command_id.hex()} 不匹配")
                            return False
        except Exception as e:
            logger.error(f"处理响应数据失败: {e}")
        
        return False
    
    def _cleanup(self):
        """清理资源"""
        self.test_running = False
        
        # 停止指令发送器
        if self.command_sender:
            self.command_sender.stop()
            self.command_sender = None
        
        # 停止数据处理器
        if self.data_processor:
            self.data_processor.stop()
            self.data_processor = None
        
        if self.data_worker:
            self.data_worker.stop()
            self.data_worker = None
    
    def _process_responses(self):
        """处理响应数据"""
        while self.test_running:
            try:
                if self.command_sender and self.data_processor:
                    # 从响应队列获取响应
                    response_queue = self.command_sender.get_response_queue()
                    response_data = response_queue.get(timeout=0.1)
                    
                    # 将响应数据加入数据处理器
                    self.data_processor.add_data(response_data)
                    
                    # 更新指令状态
                    command = response_data['command']
                    command['status'] = 'received'
                    
                    # 通知UI更新
                    if self.on_command_updated:
                        self.on_command_updated(command, 'received')
                    
                    response_queue.task_done()
                    
            except Exception as e:
                logger.error(f"处理响应失败：{str(e)}")
                time.sleep(0.1)
    
    def _process_results(self):
        """处理数据处理结果"""
        while self.test_running:
            try:
                if self.data_processor:
                    # 从结果队列获取处理结果
                    result_queue = self.data_processor.get_result_queue()
                    result = result_queue.get(timeout=0.1)
                    
                    # 更新指令状态
                    command = result['command']
                    command['status'] = 'processed'
                    
                    # 记录测试结果
                    command_result = {
                        'index': command.get('index', 0),
                        'description': command['description'],
                        'status': 'success',
                        'send_time': command.get('send_time', time.time()),
                        'response_time': command.get('response_time', time.time()),
                        'response': result['response'].hex(),
                        'parsed_data': result['parsed_data'],
                        'result': result['result']
                    }
                    self.test_results['command_results'].append(command_result)
                    
                    # 更新统计信息
                    self.test_results['commands_sent'] += 1
                    self.test_results['data_received'] += 1
                    
                    # 通知UI更新
                    if self.on_data_processed:
                        self.on_data_processed(result)
                    
                    result_queue.task_done()
                    
            except Exception as e:
                logger.error(f"处理结果失败：{str(e)}")
                time.sleep(0.1)
    
    def get_test_results(self):
        """获取测试结果"""
        return self.test_results
