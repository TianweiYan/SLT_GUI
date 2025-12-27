from backend.logger.logger import logger
import threading
from queue import Queue
import time
from concurrent.futures import ThreadPoolExecutor

class DataProcessor:
    """数据处理器，负责处理接收到的响应数据"""
    
    def __init__(self):
        self.data_queue = Queue()
        self.result_queue = Queue()
        self.running = False
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.thread = None
        
    def start(self):
        """启动数据处理线程"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()
            logger.info("数据处理线程已启动")
    
    def stop(self):
        """停止数据处理线程"""
        self.running = False
        if self.thread:
            self.thread.join()
        self.executor.shutdown()
        logger.info("数据处理线程已停止")
    
    def add_data(self, data):
        """添加数据到处理队列
        
        Args:
            data: 待处理的数据，包含command和response字段
        """
        self.data_queue.put(data)
        logger.info(f"数据已加入处理队列：{data['command']['description']}")
    
    def _run(self):
        """数据处理线程主循环"""
        while self.running:
            try:
                # 从队列获取数据
                data = self.data_queue.get(timeout=0.1)
                
                # 提交到线程池处理
                self.executor.submit(self._process_data, data)
                
                # 任务完成
                self.data_queue.task_done()
                
            except Exception as e:
                logger.error(f"数据处理线程错误：{str(e)}")
                time.sleep(0.1)
    
    def _process_data(self, data):
        """处理数据的实际逻辑
        
        Args:
            data: 待处理的数据，包含command和response字段
        """
        try:
            command = data['command']
            response = data['response']
            
            logger.info(f"开始处理数据：{command['description']}")
            
            # 解析响应数据
            parsed_data = self._parse_response(response)
            
            # 处理数据（这里可以根据实际需求扩展）
            result = self._process_parsed_data(parsed_data, command)
            
            # 将处理结果放入结果队列
            self.result_queue.put({
                'command': command,
                'response': response,
                'parsed_data': parsed_data,
                'result': result,
                'process_time': time.time()
            })
            
            logger.info(f"数据处理完成：{command['description']}")
            
        except Exception as e:
            logger.error(f"处理数据失败：{str(e)}")
    
    def _parse_response(self, response):
        """解析响应数据
        
        Args:
            response: 原始响应数据（bytes）
            
        Returns:
            dict: 解析后的数据
        """
        parsed = {}
        
        # 解析帧头
        if len(response) >= 4:
            parsed['header'] = response[:4].hex()
            
        # 解析帧长度
        if len(response) >= 8:
            parsed['length'] = int.from_bytes(response[6:8], byteorder='big')
            
        # 解析帧ID
        if len(response) >= 12:
            parsed['frame_id'] = response[8:12].hex()
            
        # 解析数据部分
        if len(response) >= 12:
            parsed['data'] = response[12:].hex()
            
        return parsed
    
    def _process_parsed_data(self, parsed_data, command):
        """处理解析后的数据
        
        Args:
            parsed_data: 解析后的数据
            command: 原始指令
            
        Returns:
            dict: 处理结果
        """
        result = {
            'status': 'success',
            'command_id': command.get('command_id', 'unknown'),
            'data': parsed_data
        }
        
        # 这里可以根据实际需求添加更多处理逻辑
        
        return result
    
    def get_result_queue(self):
        """获取处理结果队列"""
        return self.result_queue
