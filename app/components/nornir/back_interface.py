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
from paramiko.ssh_exception import AuthenticationException

from ...common.build_result_string import build_result_string
from ...common.config import cfg


# 获取配置里定义的路径
export_path = cfg.get(cfg.nornir_export_folder)

# 检查是否路径存在，不存在则创建
if not os.path.isdir(export_path):
    os.makedirs(export_path)


class NornirTask(QObject):
    # 定义信号...
    output_signal = pyqtSignal(str)
    output2_signal = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, nr, parent=None):
        super().__init__(parent)
        self.nr = nr

    def export_conf(self, task):
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
            print('\nmy_task>>>DONE-DONE-DONE\n')


    @pyqtSlot()
    def run(self):

        # task_desc = 'TASK: Export Configuration Of Device'
        results = self.nr.run(task=self.export_conf, on_failed=True)
        # print_result(results)
        res = build_result_string(results)

        # 执行完所以子任务后向窗口发送文字
        self.output_signal.emit('\n<<<已完成nornir任务')

        # 详细信息待执行完my_task后一次性返回，单独子任务返回，线程导致乱序
        self.output2_signal.emit(res)

        # 发结束进度条提示信号
        self.finished.emit()


