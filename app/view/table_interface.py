# coding: utf-8
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QWidget
from .Ui_TableInterface import Ui_TableInterfaceForm
from ..common.nr_init import DataLoadingThread


class TableInterface(Ui_TableInterfaceForm, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.model = QStandardItemModel()

        # 设置表格列标题
        self.model.setHorizontalHeaderLabels([
            "设备名称",
            "IP地址",
            "平台",
            "型号",
            "序列号",
            "设备类型",
            "区域",
            "版本",
        ])

        # 创建数据加载线程并启动
        self.loading_thread = DataLoadingThread()
        self.loading_thread.nr_initialized.connect(self.handle_initialized_nr)
        # self.loading_thread.data_loaded.connect(self.update_ui)
        self.loading_thread.start()


    def handle_initialized_nr(self, nr):

        # 接收初始化完成的 Nornir 对象
        self.nr = nr
        inventory_list = []

        for n, h in self.nr.inventory.hosts.items():
            item_list = [n, h.hostname, h.platform, h.data['model'], h.data['sn'], h.data['device_type'],
                         h.data['area'], h.data['version']]
            inventory_list.append(item_list)

        # print(inventory_list)

        for row_data in inventory_list:
            row_items = [QStandardItem(item) for item in row_data]

            self.model.appendRow(row_items)

        self.table_view.setModel(self.model)

        # 自动调整列宽以适应内容
        # self.table_view.resizeColumnsToContents()

        # 设置特定列的列宽为 120
        header = self.table_view.horizontalHeader()
        header.resizeSection(0, 120)
        header.resizeSection(1, 120)
        header.resizeSection(2, 120)
        header.resizeSection(3, 120)




