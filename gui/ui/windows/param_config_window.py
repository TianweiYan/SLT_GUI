from PyQt5 import QtWidgets


class ParamConfigWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)

        label = QtWidgets.QLabel("参数配置界面（待实现）")
        label.setStyleSheet("font-size:18px;")

        layout.addWidget(label)
        layout.addStretch()
