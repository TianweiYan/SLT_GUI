import yaml
import os
from backend.logger.logger import logger

class ConfigLoader:
    """配置加载器"""
    
    def __init__(self, config_path=None):
        if config_path is None:
            # 默认配置文件路径
            self.config_path = os.path.join(os.path.dirname(__file__), 'settings.yaml')
        else:
            self.config_path = config_path
        
        self.config = self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            else:
                logger.warning(f"配置文件不存在: {self.config_path}")
                return self._get_default_config()
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            return self._get_default_config()
    
    def _get_default_config(self):
        """获取默认配置"""
        default_config = {
            'communication': {
                'type': 'network',  # serial或network
                'serial': {
                    'port': 'COM1',
                    'baud_rate': 115200
                },
                'network': {
                    'ip': '192.168.1.100',
                    'port': 5000
                }
            },
            'test': {
                'ping_count': 4,
                'ping_timeout': 1.0,
                'command_interval': 0.5
            }
        }
        
        # 保存默认配置
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(default_config, f, default_flow_style=False, allow_unicode=True)
            logger.info(f"已创建默认配置文件: {self.config_path}")
        except Exception as e:
            logger.error(f"保存默认配置文件失败: {e}")
        
        return default_config
    
    def get(self, key_path, default=None):
        """获取配置值
        
        Args:
            key_path: 配置键路径，如 'communication.type'
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def update(self, key_path, value):
        """更新配置值
        
        Args:
            key_path: 配置键路径，如 'communication.type'
            value: 新值
        """
        keys = key_path.split('.')
        config = self.config
        
        try:
            for key in keys[:-1]:
                config = config[key]
            config[keys[-1]] = value
            
            # 保存更新后的配置
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            
            logger.info(f"更新配置: {key_path} = {value}")
            return True
        except Exception as e:
            logger.error(f"更新配置失败: {e}")
            return False

# 创建全局配置实例
config_loader = ConfigLoader()
