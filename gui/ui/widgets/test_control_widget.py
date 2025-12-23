from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from backend.logger.logger import logger

class TestControlWidget(QtWidgets.QWidget):
    """测试控制UI组件"""
    
    # 定义信号
    sig_start_test = QtCore.pyqtSignal()
    sig_stop_test = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self.test_running = False
    
    def _init_ui(self):
        """初始化UI"""
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # 开始测试按钮
        self.btn_start_test = QtWidgets.QPushButton("开始测试")
        self.btn_start_test.setFixedSize(180, 80)
        
        # 设置按钮样式和图标
        try:
            icon_path = "gui/ui/resources/icons/auto.PNG"
            icon = QtGui.QIcon(icon_path)
            self.btn_start_test.setIcon(icon)
            self.btn_start_test.setIconSize(QtCore.QSize(48, 48))
            logger.info(f"成功加载图标: {icon_path}")
        except Exception as e:
            logger.error(f"加载图标失败: {e}")
        
        self.btn_start_test.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                border: none;
                border-radius: 8px;
                color: white;
                font-size: 12pt;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        
        layout.addWidget(self.btn_start_test, 0, QtCore.Qt.AlignCenter)
        
        # 状态显示
        self.status_label = QtWidgets.QLabel("就绪")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 10pt;
                color: #333333;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.status_label)
        
        # 连接信号
        self.btn_start_test.clicked.connect(self._on_start_test_clicked)
    
    def _on_start_test_clicked(self):
        """开始测试按钮点击事件"""
        if not self.test_running:
            self.test_running = True
            self.btn_start_test.setText("停止测试")
            self.btn_start_test.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    border: none;
                    border-radius: 8px;
                    color: white;
                    font-size: 12pt;
                    font-weight: bold;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
                QPushButton:pressed {
                    background-color: #c62828;
                }
            """)
            self.sig_start_test.emit()
        else:
            self.test_running = False
            self.btn_start_test.setText("开始测试")
            self.btn_start_test.setStyleSheet("""
                QPushButton {
                    background-color: #4caf50;
                    border: none;
                    border-radius: 8px;
                    color: white;
                    font-size: 12pt;
                    font-weight: bold;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #3d8b40;
                }
            """)
            self.sig_stop_test.emit()
    
    @pyqtSlot(str)
    def set_status(self, status_text):
        """设置状态文本"""
        self.status_label.setText(status_text)
    
    @pyqtSlot(bool)
    def set_test_running(self, running):
        """设置测试运行状态"""
        self.test_running = running
        if running:
            self.btn_start_test.setText("停止测试")
            self.btn_start_test.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    border: none;
                    border-radius: 8px;
                    color: white;
                    font-size: 12pt;
                    font-weight: bold;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
                QPushButton:pressed {
                    background-color: #c62828;
                }
            """)
        else:
            self.btn_start_test.setText("开始测试")
            self.btn_start_test.setStyleSheet("""
                QPushButton {
                    background-color: #4caf50;
                    border: none;
                    border-radius: 8px;
                    color: white;
                    font-size: 12pt;
                    font-weight: bold;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #3d8b40;
                }
            """)
