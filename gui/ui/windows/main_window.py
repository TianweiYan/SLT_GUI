from PyQt5 import QtWidgets, QtCore

from gui.ui.windows.auto_test_window import AutoTestWindow
from gui.ui.windows.param_config_window import ParamConfigWindow
from gui.ui.windows.serial_port_window import SerialPortWindow
from gui.ui.widgets.top_icon_panel import TopIconPanel


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SLT 自动测试系统")
        self.resize(1400, 900)

        self._init_ui()

    def _init_ui(self):
        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)

        main_layout = QtWidgets.QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ===== 顶部固定 Panel =====
        self.top_panel = TopIconPanel()
        main_layout.addWidget(self.top_panel)
        self.top_panel.sig_auto_test.connect(self.show_auto_test)
        self.top_panel.sig_param_cfg.connect(self.show_param_config)
        self.top_panel.sig_open_serial.connect(self.open_serial_window)


        # ===== 下方展示区（切换）=====
        self.stack = QtWidgets.QStackedWidget()
        main_layout.addWidget(self.stack, 1)

        # ===== 页面 =====
        self.page_auto_test = AutoTestWindow()
        self.page_param_cfg = ParamConfigWindow()

        self.stack.addWidget(self.page_auto_test)
        self.stack.addWidget(self.page_param_cfg)

        # 👉 默认：自动测试
        self.stack.setCurrentWidget(self.page_auto_test)

        # 串口窗口（懒加载）
        self.serial_window = None

    # ================= 顶部 Panel =================
    def _create_top_panel(self):
        panel = QtWidgets.QFrame()
        panel.setFixedHeight(80)
        panel.setStyleSheet("""
            QFrame {
                background: #f5f5f5;
                border-bottom: 2px solid #1976d2;
            }
        """)

        layout = QtWidgets.QHBoxLayout(panel)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(20)

        self.btn_param = QtWidgets.QPushButton("参数配置")
        self.btn_auto  = QtWidgets.QPushButton("自动测试")
        self.btn_serial = QtWidgets.QPushButton("打开串口")

        for btn in (self.btn_param, self.btn_auto, self.btn_serial):
            btn.setFixedSize(110, 60)
            btn.setStyleSheet("""
                QPushButton {
                    background: white;
                    border: 1px solid #9e9e9e;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #e3f2fd;
                }
            """)

        layout.addWidget(self.btn_param)
        layout.addWidget(self.btn_auto)
        layout.addWidget(self.btn_serial)
        layout.addStretch()

        # 信号
        self.btn_auto.clicked.connect(self.show_auto_test)
        self.btn_param.clicked.connect(self.show_param_config)
        self.btn_serial.clicked.connect(self.open_serial_window)

        return panel

    # ================= 切换逻辑 =================
    def show_auto_test(self):
        self.stack.setCurrentWidget(self.page_auto_test)

    def show_param_config(self):
        self.stack.setCurrentWidget(self.page_param_cfg)

    def open_serial_window(self):
        if self.serial_window is None:
            self.serial_window = SerialPortWindow()

        self.serial_window.show()
        self.serial_window.raise_()
