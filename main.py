import sys
from PyQt5.QtWidgets import QApplication
from gui.ui.windows.main_window import MainWindow
from backend.logger.logger import setup_logger

def main():
    setup_logger()
    app = QApplication(sys.argv)

    # 加载 QSS
    with open("gui/ui/resources/qss/default.qss", "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

    win = MainWindow()
    win.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
