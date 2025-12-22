from PyQt5 import QtWidgets, QtGui, QtCore
import os


class IconButton(QtWidgets.QToolButton):
    def __init__(self, text, icon_path):
        super().__init__()
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setText(text)

        if os.path.exists(icon_path):
            self.setIcon(QtGui.QIcon(icon_path))

        self.setIconSize(QtCore.QSize(36, 36))
        self.setFixedSize(90, 70)


class TopIconPanel(QtWidgets.QFrame):
    sig_auto_test = QtCore.pyqtSignal()
    sig_param_cfg = QtCore.pyqtSignal()
    sig_open_serial = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setFixedHeight(80)
        self._init_ui()

    def _init_ui(self):
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(10, 4, 10, 4)
        layout.setSpacing(15)

        base = os.path.dirname(__file__)
        icon_dir = os.path.abspath(
            os.path.join(base, "..", "resources", "icons")
        )

        self.btn_param = IconButton("参数配置",
            os.path.join(icon_dir, "settings.png"))

        self.btn_serial = IconButton("打开串口",
            os.path.join(icon_dir, "serial.png"))

        self.btn_auto = IconButton("自动测试",
            os.path.join(icon_dir, "auto.png"))

        layout.addWidget(self.btn_param)
        layout.addWidget(self.btn_serial)
        layout.addWidget(self.btn_auto)
        layout.addStretch()

        self.btn_param.clicked.connect(self.sig_param_cfg.emit)
        self.btn_auto.clicked.connect(self.sig_auto_test.emit)
        self.btn_serial.clicked.connect(self.sig_open_serial.emit)
