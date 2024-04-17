import logging
import os

from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.tasks.files import write_file
from nornir.core.exceptions import NornirExecutionError

from nornir.core.task import Task
from netmiko.exceptions import NetmikoTimeoutException

from nornir_utils.plugins.functions import print_result
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from datetime import datetime

from ...common.build_result_string import build_result_string
from ...common.config import cfg


# 获取配置里定义的路径
inventory_path = cfg.get(cfg.inventory_folder)
nornir_path = cfg.get(cfg.nornir_folder)
export_path = cfg.get(cfg.nornir_export_folder)
num_workers = cfg.get(cfg.num_workers)
is_enabled = cfg.get(cfg.logging)


# 检查是否路径存在，不存在则创建
# if not os.path.isdir(inventory_path):
#     os.makedirs(inventory_path)
# if not os.path.isdir(nornir_path):
#     os.makedirs(nornir_path)
if not os.path.isdir(export_path):
    os.makedirs(export_path)

class NornirTask(QObject):
    # 发送简要结果显示到res_show
    output_signal = pyqtSignal(str)
    # 发送详细结果显示到res2_show
    output2_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.nr = InitNornir(
            runner={
                "plugin": "threaded",
                "options": {
                    "num_workers": num_workers,
                },
            },
            # inventory={
            #     "plugin": "SimpleInventory",
            #     "options": {
            #         "host_file": inventory_path + "/hosts.yaml",
            #         "group_file": inventory_path + "/groups.yaml",
            #         "defaults_file": inventory_path + "/defaults.yaml"
            #     },
            # },
            inventory={
                "plugin": "ExcelInventory",
                "options": {
                    "excel_file": inventory_path + "/inventory_unprotected.xlsx",
                },
            },
            logging={
                "enabled": is_enabled,
                "level": "INFO",
                "log_file": nornir_path + "/nornir.log"
            },
        )

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////

    @pyqtSlot()
    def run_task(self):
        # Nornir 任务
        res = self.nr.run(task=self.my_task)
        res = build_result_string(res)

        # 执行完所以子任务后向窗口发送文字
        self.output_signal.emit('\n<<<已完成nornir任务')
        # 详细信息待执行完my_task后一次性返回，单独子任务返回，线程导致乱序
        self.output2_signal.emit(res)

        print('run_task>>>DONE')

    def my_task(self, task):

        try:
            cmds = task.host.get('display').split(',')
            name = task.host.name
            ip = task.host.hostname
            time_str = datetime.now().strftime("%H%M%S")
            output = ''
            for cmd in cmds:
                output += '\n' + '=' * 100 + '\n' + cmd.center(100, '=') + '\n'
                display_res = task.run(task=netmiko_send_command,
                                       command_string=cmd)
                output += display_res[0].result

            # 发送数据显示在窗口
            self.output_signal.emit('设备：{}\tIP地址：{}\t状态：已完成'.format(name, ip))

            file_path = os.path.normpath(
                os.path.join(export_path, '{}_{}_{}.txt'.format(name, ip, time_str)))

            display_res_write = task.run(task=write_file,
                                         filename=file_path,
                                         content=output)
            print('my_task>>>DONE')
            # if display_res_write:
            #     print('write 0kkkk')

        except Exception as e:
            # raise Exception(e)
            # print(str(e))
            e_first_line = task.results[-1].exception.args[0].split("\n")[0]
            # 发送数据显示在窗口
            self.output_signal.emit('设备：{}\tIP地址：{}\t状态：未完成(可能的原因：{})'.format(name, ip, e_first_line))
            print('my_task>>>DONE-DONE-DONE')
