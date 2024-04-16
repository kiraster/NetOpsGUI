# coding: utf-8
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect
from qfluentwidgets import FluentIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import threading
from ..components.nornir.back_interface import NornirTask
from .Ui_AutoInterface import Ui_AutoInterfaceForm


class AutoInterface(Ui_AutoInterfaceForm, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.nornir_thread = None  # 增加一个线程对象成员变量

        # set the icon of button
        self.start_btn.setIcon(FluentIcon.PLAY)

        self.start_btn.clicked.connect(self.run_nornir_task)  # 绑定按钮点击事件

        # add shadow effect to card
        # self.setShadowEffect(self.paraCard)
        # self.setShadowEffect(self.resCard)

    @pyqtSlot()
    def run_nornir_task(self):

        self.res_show.clear()  # 清空文本框
        self.res2_show.clear()  # 清空文本框
        self.res_show.setPlainText('正在执行nornir任务，可稍后回来查看结果>>>\n')
        self.res2_show.setPlainText('详细信息显示>>>\n')

        # 创建一个新的线程来执行 Nornir 任务
        self.nornir_thread = threading.Thread(target=self._run_nornir_task)
        self.nornir_thread.start()

    def _run_nornir_task(self):
        nornir_task = NornirTask()
        nornir_task.output_signal.connect(self.update_text_edit)
        nornir_task.output2_signal.connect(self.update_text2_edit)
        nornir_task.run_task()

    @pyqtSlot(str)
    def update_text_edit(self, text):
        self.res_show.appendPlainText(text)

    @pyqtSlot(str)
    def update_text2_edit(self, text):
        self.res2_show.appendPlainText(text)

    # def setShadowEffect(self, card: QWidget):
    #     shadowEffect = QGraphicsDropShadowEffect(self)
    #     shadowEffect.setColor(QColor(0, 0, 0, 15))
    #     shadowEffect.setBlurRadius(10)
    #     shadowEffect.setOffset(0, 0)
    #     card.setGraphicsEffect(shadowEffect)
