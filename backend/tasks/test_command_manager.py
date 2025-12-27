from backend.logger.logger import logger
import os
import yaml

class TestCommandManager:
    """测试指令管理器，负责加载和管理测试指令"""
    
    def __init__(self, config_file_path=None):
        """初始化
        
        Args:
            config_file_path: 测试指令配置文件路径
        """
        if config_file_path is None:
            # 默认配置文件路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_file_path = os.path.join(current_dir, 'test_commands.yaml')
        
        self.config_file_path = config_file_path
        self.commands = []  # 存储指令列表
        self.response_frames = []  # 存储响应帧列表
        self.load_commands()
    
    def load_commands(self):
        """从配置文件加载测试指令"""
        try:
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            self.commands.clear()
            self.response_frames.clear()
            
            # 加载发送指令
            if 'commands' in config:
                for cmd in config['commands']:
                    try:
                        description = cmd['description']
                        hex_data_str = cmd['hex_data'].replace(' ', '')
                        
                        # 转换为字节数据
                        if len(hex_data_str) % 2 != 0:
                            logger.warning(f"解析指令失败：{description}（十六进制数据长度为奇数）")
                            continue
                        
                        # 将十六进制字符串转换为字节
                        data = bytes.fromhex(hex_data_str)
                        
                        # 添加到指令列表
                        self.commands.append({
                            'description': description,
                            'data': data,
                            'hex_str': hex_data_str,
                            'status': 'pending'  # pending, sent, success, failed
                        })
                        
                        logger.info(f"加载指令成功：{description} - {hex_data_str}")
                        
                    except Exception as e:
                        logger.error(f"解析指令失败：{cmd} - {str(e)}")
            
            # 加载响应帧
            if 'response_frames' in config:
                for frame in config['response_frames']:
                    try:
                        description = frame['description']
                        hex_data_str = frame['hex_data'].replace(' ', '')
                        
                        # 转换为字节数据
                        if len(hex_data_str) % 2 != 0:
                            logger.warning(f"解析响应帧失败：{description}（十六进制数据长度为奇数）")
                            continue
                        
                        # 将十六进制字符串转换为字节
                        data = bytes.fromhex(hex_data_str)
                        
                        # 添加到响应帧列表
                        self.response_frames.append({
                            'description': description,
                            'data': data,
                            'hex_str': hex_data_str
                        })
                        
                        logger.info(f"加载响应帧成功：{description} - {hex_data_str}")
                        
                    except Exception as e:
                        logger.error(f"解析响应帧失败：{frame} - {str(e)}")
            
            logger.info(f"成功加载 {len(self.commands)} 条测试指令和 {len(self.response_frames)} 条响应帧")
            
        except Exception as e:
            logger.error(f"加载测试指令配置文件失败：{str(e)}")
            raise
    
    def get_commands(self):
        """获取所有测试指令
        
        Returns:
            list: 测试指令列表
        """
        return self.commands
    
    def get_command_by_index(self, index):
        """根据索引获取测试指令
        
        Args:
            index: 指令索引
            
        Returns:
            dict: 测试指令
        """
        if 0 <= index < len(self.commands):
            return self.commands[index]
        return None
    
    def update_command_status(self, index, status):
        """更新指令状态
        
        Args:
            index: 指令索引
            status: 新状态（pending, sent, success, failed）
        """
        if 0 <= index < len(self.commands):
            self.commands[index]['status'] = status
    
    def get_commands_count(self):
        """获取指令总数
        
        Returns:
            int: 指令总数
        """
        return len(self.commands)
    
    def reload_commands(self):
        """重新加载测试指令
        """
        self.load_commands()
    
    def get_response_frames(self):
        """获取所有响应帧
        
        Returns:
            list: 响应帧列表
        """
        return self.response_frames
    
    def get_response_frame_by_index(self, index):
        """根据索引获取响应帧
        
        Args:
            index: 响应帧索引
            
        Returns:
            dict: 响应帧
        """
        if 0 <= index < len(self.response_frames):
            return self.response_frames[index]
        return None
