from PyQt5 import QtWidgets


class SerialPortWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("串口调试")
        self.resize(600, 400)

        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(QtWidgets.QLabel("串口配置 / 收发显示（待实现）"))
