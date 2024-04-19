# coding:utf-8
import os
from PyQt5.QtCore import QThread, pyqtSignal
from ..common.config import cfg
from nornir import InitNornir

class DataLoadingThread(QThread):
    data_loaded = pyqtSignal(list, list, list)  # 定义信号，用于发送加载完的数据

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def run(self):
        # 获取配置里定义的路径和参数
        inventory_file = cfg.get(cfg.inventory_file)
        nornir_path = cfg.get(cfg.nornir_folder)
        num_workers = cfg.get(cfg.num_workers)
        is_enabled = cfg.get(cfg.logging)

        platform_list = []
        model_list = []
        area_list = []

        # 检查并创建不存在的路径
        export_path = cfg.get(cfg.nornir_export_folder)
        if not os.path.isdir(export_path):
            os.makedirs(export_path)

        # 在子线程中加载数据
        nr = InitNornir(
            runner={
                "plugin": "threaded",
                "options": {
                    "num_workers": num_workers,
                },
            },
            inventory={
                "plugin": "ExcelInventory",
                "options": {
                    "excel_file": inventory_file,
                },
            },
            logging={
                "enabled": is_enabled,
                "level": "INFO",
                "log_file": nornir_path + "/nornir.log"
            },
        )

        hosts = nr.inventory.hosts.items()
        for n, h in hosts:
            platform_list.append(h.platform)
            model_list.append(h.data['model'])
            area_list.append(h.data['area'])

        # 去重
        platform_list = list(set(platform_list))
        model_list = list(set(model_list))
        area_list = list(set(area_list))

        # 发送信号，将加载完的数据发送到主线程
        self.data_loaded.emit(platform_list, model_list, area_list)
