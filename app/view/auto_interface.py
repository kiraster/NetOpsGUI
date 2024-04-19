# coding: utf-8
import os
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect
from qfluentwidgets import FluentIcon, StateToolTip, ComboBox
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from nornir import InitNornir
import threading
from ..components.nornir.back_interface import NornirTask
from .Ui_AutoInterface import Ui_AutoInterfaceForm
from ..common.config import cfg
from ..common.nr_init import DataLoadingThread

# # 获取配置里定义的路径
# # inventory_path = cfg.get(cfg.inventory_folder)
# inventory_file = cfg.get(cfg.inventory_file)
# nornir_path = cfg.get(cfg.nornir_folder)
# export_path = cfg.get(cfg.nornir_export_folder)
# num_workers = cfg.get(cfg.num_workers)
# is_enabled = cfg.get(cfg.logging)
#
#
# # 检查是否路径存在，不存在则创建
# # if not os.path.isdir(inventory_path):
# #     os.makedirs(inventory_path)
# # if not os.path.isdir(nornir_path):
# #     os.makedirs(nornir_path)
# if not os.path.isdir(export_path):
#     os.makedirs(export_path)


class AutoInterface(Ui_AutoInterfaceForm, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        # ////////////////////////////////////////////////////////////////////////////////////////////////////
        # nornir 初始化
        # self.nr = InitNornir(
        #     runner={
        #         "plugin": "threaded",
        #         "options": {
        #             "num_workers": num_workers,
        #         },
        #     },
        #     # inventory={
        #     #     "plugin": "SimpleInventory",
        #     #     "options": {
        #     #         "host_file": inventory_path + "/hosts.yaml",
        #     #         "group_file": inventory_path + "/groups.yaml",
        #     #         "defaults_file": inventory_path + "/defaults.yaml"
        #     #     },
        #     # },
        #     inventory={
        #         "plugin": "ExcelInventory",
        #         "options": {
        #             "excel_file": inventory_file,
        #         },
        #     },
        #     logging={
        #         "enabled": is_enabled,
        #         "level": "INFO",
        #         "log_file": nornir_path + "/nornir.log"
        #     },
        # )
        # # ////////////////////////////////////////////////////////////////////////////////////////////////////
        #
        # # 定义列表接收内容
        # self.platform_list = []
        # self.model_list = []
        # self.area_list = []
        # hosts = self.nr.inventory.hosts.items()
        # # print(hosts)
        # for n, h in hosts:
        #     # 打印所以platform
        #     # print(h.platform)
        #     self.platform_list.append(h.platform)
        #     self.model_list.append(h.data['model'])
        #     self.area_list.append(h.data['area'])
        #
        # # 去重
        # self.platform_list = list(set(self.platform_list))
        # self.model_list = list(set(self.model_list))
        # self.area_list = list(set(self.area_list))

        # print(self.platform_list)
        # print(self.model_list)
        # print(self.area_list)

        # 添加ComboBox 下拉按钮内容，利用以上列表内容 >>>>>>>>>>>>>>>>>>>>>>>>>>>

        # # 数据源下拉按钮
        # self.data_combobox.setPlaceholderText('数据源-1')
        # # self.data_combobox.addItems(self.platform_list)
        # # self.data_combobox.setCurrentIndex(-1)
        # # 平台下拉按钮
        # self.platform_combobox.setPlaceholderText('全部')
        # self.platform_combobox.addItems(self.platform_list)
        # self.platform_combobox.setCurrentIndex(-1)
        # # 型号下拉按钮
        # self.model_combobox.setPlaceholderText('全部')
        # self.model_combobox.addItems(self.model_list)
        # self.model_combobox.setCurrentIndex(-1)
        # # 区域下拉按钮
        # self.area_combobox.setPlaceholderText('全部')
        # self.area_combobox.addItems(self.area_list)
        # self.area_combobox.setCurrentIndex(-1)

        # 定义列表接收内容
        self.platform_list = []
        self.model_list = []
        self.area_list = []

        # 创建数据加载线程并启动
        self.loading_thread = DataLoadingThread()
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

        # 显示开始进度提示条
        self.state_tooltip = StateToolTip('正在后台执行任务', '可稍后回来查看结果', self)
        self.state_tooltip.move(640, 25)
        self.state_tooltip.show()

        # 创建一个新的线程来执行 Nornir 任务
        self.nornir_thread = threading.Thread(target=self._run_nornir_task)
        self.nornir_thread.start()

    def _run_nornir_task(self):
        nornir_task = NornirTask()
        nornir_task.output_signal.connect(self.update_text_edit)
        nornir_task.output2_signal.connect(self.update_text2_edit)
        nornir_task.run_task()

        # 显示结束进度提示条
        self.state_tooltip.setTitle('后台任务已完成')
        self.state_tooltip.setContent('在下方查看运行结果')
        self.state_tooltip.setState(True)
        self.state_tooltip = None

    @pyqtSlot(str)
    def update_text_edit(self, text):
        self.res_show.appendPlainText(text)

    @pyqtSlot(str)
    def update_text2_edit(self, text):
        self.res2_show.appendPlainText(text)

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
