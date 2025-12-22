from PyQt5 import QtWidgets, QtCore


class PowerMonitorPanel(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super().__init__("电压电流及温度信号监测", parent)
        self._init_ui()

    def _init_ui(self):
        self.setMinimumWidth(300)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(16)

        # ================= 温度 =================
        temp_layout = QtWidgets.QHBoxLayout()

        lbl_temp_name = QtWidgets.QLabel("SIP芯片温度值")
        self.lbl_temp_value = QtWidgets.QLabel("0")
        lbl_temp_unit = QtWidgets.QLabel("℃")

        self._style_value_label(self.lbl_temp_value, "#ffcc99")

        temp_layout.addWidget(lbl_temp_name)
        temp_layout.addStretch()
        temp_layout.addWidget(self.lbl_temp_value)
        temp_layout.addWidget(lbl_temp_unit)

        main_layout.addLayout(temp_layout)

        # ================= 总电流 =================
        current_layout = QtWidgets.QHBoxLayout()

        lbl_cur_name = QtWidgets.QLabel("16路供电总电流值")
        self.lbl_cur_value = QtWidgets.QLabel("0")
        lbl_cur_unit = QtWidgets.QLabel("A")

        self._style_value_label(self.lbl_cur_value, "#66ff99")

        current_layout.addWidget(lbl_cur_name)
        current_layout.addStretch()
        current_layout.addWidget(self.lbl_cur_value)
        current_layout.addWidget(lbl_cur_unit)

        main_layout.addLayout(current_layout)

        # ================= 总功率 =================
        power_layout = QtWidgets.QHBoxLayout()

        lbl_pwr_name = QtWidgets.QLabel("16路供电总功率值")
        self.lbl_pwr_value = QtWidgets.QLabel("0")
        lbl_pwr_unit = QtWidgets.QLabel("W")

        self._style_value_label(self.lbl_pwr_value, "#99ddff")

        power_layout.addWidget(lbl_pwr_name)
        power_layout.addStretch()
        power_layout.addWidget(self.lbl_pwr_value)
        power_layout.addWidget(lbl_pwr_unit)

        main_layout.addLayout(power_layout)

        main_layout.addStretch()

    def _style_value_label(self, label: QtWidgets.QLabel, bg_color: str):
        label.setFixedWidth(80)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                border: 1px solid #9e9e9e;
                font-weight: bold;
                font-size: 14px;
            }}
        """)

    # ====== 对外接口（后面联动数据） ======
    def set_temperature(self, value: float):
        self.lbl_temp_value.setText(f"{value:.1f}")

    def set_total_current(self, value: float):
        self.lbl_cur_value.setText(f"{value:.3f}")

    def set_total_power(self, value: float):
        self.lbl_pwr_value.setText(f"{value:.3f}")
