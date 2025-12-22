# -*- coding: utf-8 -*-
# Auto-generated style UI (LabVIEW-like layout)

from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1400, 900)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.main_layout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(6, 6, 6, 6)

        # ================= 左侧：控制区 =================
        self.left_panel = QtWidgets.QFrame(self.centralwidget)
        self.left_panel.setMinimumWidth(260)
        self.left_panel.setFrameShape(QtWidgets.QFrame.StyledPanel)

        self.left_layout = QtWidgets.QVBoxLayout(self.left_panel)

        self.control_group = QtWidgets.QGroupBox("Test Control")
        self.control_layout = QtWidgets.QVBoxLayout(self.control_group)

        self.btn_start = QtWidgets.QPushButton("START")
        self.btn_stop = QtWidgets.QPushButton("STOP")
        self.btn_browse = QtWidgets.QPushButton("Browse Config")

        self.control_layout.addWidget(self.btn_start)
        self.control_layout.addWidget(self.btn_stop)
        self.control_layout.addSpacing(10)
        self.control_layout.addWidget(self.btn_browse)
        self.control_layout.addStretch()

        self.left_layout.addWidget(self.control_group)

        self.log_group = QtWidgets.QGroupBox("Log")
        self.log_layout = QtWidgets.QVBoxLayout(self.log_group)
        self.text_log = QtWidgets.QTextEdit()
        self.text_log.setReadOnly(True)
        self.log_layout.addWidget(self.text_log)

        self.left_layout.addWidget(self.log_group)

        # ================= 中间：波形区 =================
        self.center_panel = QtWidgets.QFrame(self.centralwidget)
        self.center_panel.setFrameShape(QtWidgets.QFrame.StyledPanel)

        self.center_layout = QtWidgets.QVBoxLayout(self.center_panel)

        self.wave_group = QtWidgets.QGroupBox("AD Waveform")
        self.wave_layout = QtWidgets.QVBoxLayout(self.wave_group)

        self.plot_time = QtWidgets.QFrame()
        self.plot_time.setMinimumHeight(280)

        self.plot_freq = QtWidgets.QFrame()
        self.plot_freq.setMinimumHeight(280)

        self.wave_layout.addWidget(self.plot_time)
        self.wave_layout.addWidget(self.plot_freq)

        self.center_layout.addWidget(self.wave_group)

        # ================= 右侧：参数显示 =================
        self.right_panel = QtWidgets.QFrame(self.centralwidget)
        self.right_panel.setMinimumWidth(300)
        self.right_panel.setFrameShape(QtWidgets.QFrame.StyledPanel)

        self.right_layout = QtWidgets.QVBoxLayout(self.right_panel)

        self.metrics_group = QtWidgets.QGroupBox("AD Metrics")
        self.metrics_layout = QtWidgets.QGridLayout(self.metrics_group)

        labels = [
            "RMS", "Peak", "SNR",
            "THD", "SFDR", "ENOB"
        ]

        self.metric_value_labels = {}

        for row, name in enumerate(labels):
            lbl_name = QtWidgets.QLabel(name + ":")
            lbl_val = QtWidgets.QLabel("N/A")
            lbl_val.setMinimumWidth(100)

            self.metrics_layout.addWidget(lbl_name, row, 0)
            self.metrics_layout.addWidget(lbl_val, row, 1)

            self.metric_value_labels[name] = lbl_val

        self.right_layout.addWidget(self.metrics_group)
        self.right_layout.addStretch()

        # ================= 组合 =================
        self.main_layout.addWidget(self.left_panel)
        self.main_layout.addWidget(self.center_panel, 1)
        self.main_layout.addWidget(self.right_panel)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("SLT GUI")
