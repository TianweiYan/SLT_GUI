from backend.logger.logger import logger
import threading
import time
from queue import Queue

class CommandSender:
    """指令发送器，负责按顺序发送指令并等待响应"""
    
    def __init__(self, communication_interface):
        self.comm_interface = communication_interface
        self.command_queue = Queue()
        self.response_queue = Queue()
        self.running = False
        self.thread = None
        self.current_command = None
        
    def start(self):
        """启动指令发送线程"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()
            logger.info("指令发送线程已启动")
    
    def stop(self):
        """停止指令发送线程"""
        self.running = False
        if self.thread:
            self.thread.join()
            logger.info("指令发送线程已停止")
    
    def send_command(self, command):
        """发送指令（线程安全）
        
        Args:
            command: 指令字典，包含description、data等字段
        """
        self.command_queue.put(command)
        logger.info(f"指令已加入队列：{command['description']}")
    
    def _run(self):
        """指令发送线程主循环"""
        while self.running:
            try:
                # 从队列获取指令
                command = self.command_queue.get(timeout=0.1)
                
                # 记录当前发送的指令
                self.current_command = command
                command['status'] = 'sending'
                
                logger.info(f"开始发送指令：{command['description']}")
                
                # 发送指令
                self.comm_interface.send(command['data'])
                
                command['status'] = 'sent'
                command['send_time'] = time.time()
                
                # 等待响应（可以设置超时）
                response = self.comm_interface.receive(timeout=2.0)
                
                if response:
                    command['status'] = 'success'
                    command['response_time'] = time.time()
                    command['response_data'] = response
                    logger.info(f"指令发送成功并收到响应：{command['description']}")
                    
                    # 将响应放入队列供处理线程使用
                    self.response_queue.put({
                        'command': command,
                        'response': response
                    })
                else:
                    command['status'] = 'failed'
                    command['error'] = '未收到响应'
                    logger.warning(f"指令发送后未收到响应：{command['description']}")
                
                # 任务完成
                self.command_queue.task_done()
                
                # 指令间隔
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"指令发送线程错误：{str(e)}")
                time.sleep(0.1)
    
    def get_current_command(self):
        """获取当前正在处理的指令"""
        return self.current_command
    
    def get_response_queue(self):
        """获取响应队列"""
        return self.response_queue
