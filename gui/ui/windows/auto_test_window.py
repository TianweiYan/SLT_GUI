from PyQt5 import QtWidgets, QtCore
from gui.ui.widgets.power_monitor_panel import PowerMonitorPanel
from gui.ui.widgets.test_control_widget import TestControlWidget
from backend.tasks.test_manager import TestManager
from backend.logger.logger import logger


class AutoTestWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._init_test_manager()

    def _init_ui(self):
        """初始化UI"""
        main_layout = QtWidgets.QHBoxLayout(self)

        # 左侧：测试控制区
        self.left_panel = QtWidgets.QFrame()
        main_layout.addWidget(self.left_panel, 2)
        
        left_layout = QtWidgets.QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(20)

        # 添加测试控制组件
        self.test_control_widget = TestControlWidget()
        left_layout.addWidget(self.test_control_widget, 0, QtCore.Qt.AlignCenter)
        
        left_layout.addStretch()

        # 右侧：监测面板
        self.monitor_panel = PowerMonitorPanel()
        main_layout.addWidget(self.monitor_panel, 1)

        # ===== 初始 Demo 数据 =====
        self.monitor_panel.set_temperature(36.5)
        self.monitor_panel.set_total_current(7.147)
        self.monitor_panel.set_total_power(8.382)

    def _init_test_manager(self):
        """初始化测试管理器"""
        self.test_manager = TestManager()
        
        # 连接信号
        self.test_control_widget.sig_start_test.connect(self._on_start_test)
        self.test_control_widget.sig_stop_test.connect(self._on_stop_test)

    def _on_start_test(self):
        """开始测试"""
        logger.info("用户点击开始测试")
        self.test_manager.start_test(
            on_status_update=self._update_status,
            on_error=self._show_error,
            on_test_complete=self._on_test_complete
        )

    def _on_stop_test(self):
        """停止测试"""
        logger.info("用户点击停止测试")
        self.test_manager.stop_test()
        self.test_control_widget.set_status("测试已停止")

    def _update_status(self, status_text):
        """更新状态显示"""
        logger.info(f"测试状态更新: {status_text}")
        QtCore.QMetaObject.invokeMethod(self.test_control_widget, "set_status", 
                                      QtCore.Q_ARG(str, status_text))

    def _show_error(self, error_message):
        """显示错误信息"""
        logger.error(f"测试错误: {error_message}")
        QtCore.QMetaObject.invokeMethod(self.test_control_widget, "set_status", 
                                      QtCore.Q_ARG(str, "测试失败"))
        
        # 在主线程显示错误消息框
        def show_error_dialog():
            QtWidgets.QMessageBox.critical(self, "测试错误", error_message)
            
        QtCore.QMetaObject.invokeMethod(self, "_show_error_dialog", 
                                      QtCore.Q_ARG(str, error_message))
    
    def _show_error_dialog(self, error_message):
        """在主线程显示错误消息框"""
        QtWidgets.QMessageBox.critical(self, "测试错误", error_message)

    def _on_test_complete(self, test_results):
        """测试完成处理"""
        logger.info(f"测试完成，结果: {test_results}")
        
        # 更新测试控件状态
        QtCore.QMetaObject.invokeMethod(self.test_control_widget, "set_test_running", 
                                      QtCore.Q_ARG(bool, False))
        
        # 可以在这里添加测试结果的进一步处理
        # 例如保存到数据库、生成报告等

    def closeEvent(self, event):
        """窗口关闭时清理资源"""
        self.test_manager.stop_test()
        super().closeEvent(event)
