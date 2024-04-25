# coding: utf-8
import os
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect
from qfluentwidgets import FluentIcon, StateToolTip, ComboBox
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread, Qt
from nornir import InitNornir
import threading
from ..components.nornir.back_interface import NornirTask
from .Ui_AutoInterface import Ui_AutoInterfaceForm
from nornir.core.filter import F
from ..common.nr_filter import filter_nornir
from ..common.config import cfg
from ..common.nr_init import DataLoadingThread


class AutoInterface(Ui_AutoInterfaceForm, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.nornir_task = None
        self.nr = None
        self.setupUi(self)

        # 显示开始进度提示条
        self.nornir_init_tooltip = StateToolTip('nornir正在初始化中', '稍等片刻', self)
        self.nornir_init_tooltip.move(640, 25)
        self.nornir_init_tooltip.show()

        # 定义列表接收内容
        self.platform_list = []
        self.model_list = []
        self.area_list = []

        # 创建数据加载线程并启动
        self.loading_thread = DataLoadingThread()
        self.loading_thread.nr_initialized.connect(self.handle_initialized_nr)
        self.loading_thread.data_loaded.connect(self.update_ui)
        self.loading_thread.start()


        # 清空筛选条件
        self.clear_btn.clicked.connect(self.clear_filter)

        self.nornir_thread = None  # 增加一个线程对象成员变量

        # set the icon of button
        self.start_btn.setIcon(FluentIcon.PLAY)
        self.start_btn.clicked.connect(self.run_nornir_task)

        # 添加批量操作执行后进度提示条
        self.state_tooltip = None

        # add shadow effect to card
        # self.setShadowEffect(self.paraCard)
        # self.setShadowEffect(self.resCard)

    @pyqtSlot()
    def run_nornir_task(self):

        self.res_show.clear()  # 清空文本框
        self.res2_show.clear()  # 清空文本框
        self.res_show.setPlainText('正在执行nornir任务，可稍后回来查看结果>>>\n')
        self.res2_show.setPlainText('详细信息显示>>>\n')

        # nornir对象过滤
        ip_value, platform_value, model_value, area_value = self.get_combobox_condition()
        # print("ip:", ip_value)
        # print("Platform:", platform_value)
        # print("Model:", model_value)
        # print("Area:", area_value)
        self.new_nr = filter_nornir(self.nr, ip_value, platform_value, model_value, area_value)
        # print(self.new_nr.inventory.hosts)
        if self.new_nr.inventory.hosts:
            # 显示开始进度提示条
            self.state_tooltip = StateToolTip('正在后台执行任务', '可稍后回来查看结果', self)
            self.state_tooltip.move(640, 25)
            self.state_tooltip.show()
            # 创建一个新的QThread来执行Nornir 任务
            self.nornir_thread = QThread()
            self.nornir_worker = NornirTask(self.new_nr)  # 传递nr对象
            self.nornir_worker.moveToThread(self.nornir_thread)
            # 连接信号
            self.nornir_worker.output_signal.connect(self.update_text_edit)
            self.nornir_worker.output2_signal.connect(self.update_text2_edit)
            self.nornir_worker.finished.connect(self.on_nornir_finished)  # 新增槽函数
            self.nornir_thread.started.connect(self.nornir_worker.run)
            self.nornir_thread.start()
        else:
            self.res_show.setPlainText('没有符合条件的结果>>>\n')

    @pyqtSlot(str)
    def update_text_edit(self, text):
        self.res_show.appendPlainText(text)

    @pyqtSlot(str)
    def update_text2_edit(self, text):
        self.res2_show.appendPlainText(text)

    @pyqtSlot()
    def on_nornir_finished(self):  # 新增槽函数

        self.state_tooltip.setTitle('后台任务已完成')
        self.state_tooltip.setContent('在下方查看运行结果')
        self.state_tooltip.setState(True)
        self.state_tooltip = None
        self.nornir_thread.quit()
        self.nornir_thread.wait()
        self.nornir_thread.deleteLater()
        self.nornir_thread = None

    # @pyqtSlot()
    def update_ui(self, platform_list, model_list, area_list):

        # 在主线程中更新界面
        self.platform_list = platform_list
        self.model_list = model_list
        self.area_list = area_list

        # 添加ComboBox 下拉按钮内容
        self.platform_combobox.setPlaceholderText('全部')
        self.platform_combobox.addItems(self.platform_list)
        self.platform_combobox.setCurrentIndex(-1)
        self.model_combobox.setPlaceholderText('全部')
        self.model_combobox.addItems(self.model_list)
        self.model_combobox.setCurrentIndex(-1)
        self.area_combobox.setPlaceholderText('全部')
        self.area_combobox.addItems(self.area_list)
        self.area_combobox.setCurrentIndex(-1)

    def get_combobox_condition(self):

        # 获取 ComboBox 的当前值
        ip_value = self.ip_lineedit.text()
        platform_value = self.platform_combobox.currentText()
        model_value = self.model_combobox.currentText()
        area_value = self.area_combobox.currentText()

        # 检查值是否为空字符串，如果是，则将其设为 None
        ip_value = None if ip_value == "" else ip_value
        platform_value = None if platform_value == "" else platform_value
        model_value = None if model_value == "" else model_value
        area_value = None if area_value == "" else area_value
        return ip_value, platform_value, model_value, area_value

    # @pyqtSlot()
    def handle_initialized_nr(self, nr):

        # 接收初始化完成的 Nornir 对象
        # print("Nornir initialized:", nr)
        self.nr = nr
        # self.res_show.setPlainText('nornir初始化已完成\n')
        # 显示nornir初始化已完成进度提示条
        self.nornir_init_tooltip.setTitle('nornir初始化已完成')
        self.nornir_init_tooltip.setContent('GoGoGo')
        self.nornir_init_tooltip.setState(True)
        self.nornir_init_tooltip = None
        self.start_btn.setEnabled(True)

    def clear_filter(self):

        # 清空ComboBox
        self.platform_combobox.setCurrentIndex(-1)
        self.model_combobox.setCurrentIndex(-1)
        self.area_combobox.setCurrentIndex(-1)
        # 清空LineEdit
        self.ip_lineedit.clear()

    # def setShadowEffect(self, card: QWidget):
    #     shadowEffect = QGraphicsDropShadowEffect(self)
    #     shadowEffect.setColor(QColor(0, 0, 0, 15))
    #     shadowEffect.setBlurRadius(10)
    #     shadowEffect.setOffset(0, 0)
    #     card.setGraphicsEffect(shadowEffect)