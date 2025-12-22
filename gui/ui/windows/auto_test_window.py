from PyQt5 import QtWidgets
from gui.ui.widgets.power_monitor_panel import PowerMonitorPanel


class AutoTestWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        main_layout = QtWidgets.QHBoxLayout(self)

        # 左侧：自动测试主体
        self.left_panel = QtWidgets.QFrame()
        main_layout.addWidget(self.left_panel, 2)

        # 右侧：监测面板（1/3）
        self.monitor_panel = PowerMonitorPanel()
        main_layout.addWidget(self.monitor_panel, 1)

        # ===== Demo 数据 =====
        self.monitor_panel.set_temperature(36.5)
        self.monitor_panel.set_total_current(7.147)
        self.monitor_panel.set_total_power(8.382)
