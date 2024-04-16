# coding: utf-8
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtGui import QIcon, QDesktopServices, QColor
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout

from qfluentwidgets import (NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow,
                            SplashScreen)
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, SplitFluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont)
from PyQt5.QtCore import Qt, QUrl
from qfluentwidgets import FluentIcon as FIF

from .gallery_interface import GalleryInterface
from .setting_interface import SettingInterface
from ..common.config import ZH_SUPPORT_URL, EN_SUPPORT_URL, cfg
from ..common.icon import Icon
from ..common.signal_bus import signalBus
from ..common.translator import Translator
from ..common import resource

from app.view.auto_interface import AutoInterface


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))

        # !IMPORTANT: leave some space for title bar
        self.hBoxLayout.setContentsMargins(0, 32, 0, 0)

class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        # 创建子接口，替换文字显示
        self.auto_interface = AutoInterface(self)
        self.device_list_interface = Widget('设备列表接口', self)
        self.get_port_interface = Widget('获取端口信息接口', self)
        self.get_diagnosis_interface = Widget('导出诊断信息和日志接口', self)
        self.centos_sec_interface = Widget('CentOS/KylinSec安全基线检查和加固接口', self)

        self.settingInterface = SettingInterface(self)

        # enable acrylic effect
        self.navigationInterface.setAcrylicEnabled(True)
        self.setCustomBackgroundColor(QColor(240, 244, 249), QColor(32, 32, 32))

        self.connectSignalToSlot()

        # add items to navigation interface
        self.initNavigation()
        self.initWindow()
        # self.splashScreen.finish()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signalBus.switchToSampleCard.connect(self.switchToSample)
        signalBus.supportSignal.connect(self.onSupport)

    def initNavigation(self):
        # add navigation items
        t = Translator()
        self.addSubInterface(self.auto_interface, FIF.ASTERISK, '批量操作')
        self.addSubInterface(self.device_list_interface, FIF.ALIGNMENT, '设备列表')
        self.addSubInterface(self.get_port_interface, FIF.IOT, '获取端口信息')
        self.addSubInterface(self.get_diagnosis_interface, FIF.SEND, '导出诊断信息和日志')
        self.addSubInterface(self.centos_sec_interface, FIF.DEVELOPER_TOOLS, 'CentOS/KylinSec安全')

        self.navigationInterface.addSeparator()

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('Kiraster', 'app/resource/images/kiraster.jpg'),
            onClick=self.show_message_box,
            position=NavigationItemPosition.BOTTOM,
        )
        # self.addSubInterface(
        #     self.settingInterface, FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM)
        self.addSubInterface(
            self.settingInterface, FIF.SETTING, self.tr('Settings'), NavigationItemPosition.BOTTOM)

    def initWindow(self):

        self.resize(960, 780)
        self.setMinimumWidth(760)
        # self.setWindowIcon(QIcon('app/resource/logo.png'))
        self.setWindowTitle('NetOpsGUI (NetOps图形化版本)')

        self.setMicaEffectEnabled(cfg.get(cfg.mica_enabled))

        # # create splash screen 不使用，这个卡
        # self.splashScreen = SplashScreen(self.windowIcon(), self)
        # self.splashScreen.setIconSize(QSize(106, 106))
        # self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

    def show_message_box(self):
        w = MessageBox(
            '讲多谢,唔讲补一枪.',
            "名称：NetOpsGUI\n版本：v1.0.1_alpha\nGitHub：https://github.com/kiraster/\nEmail：kir_aster@foxmail.com\n\n说明：\n1、在nornir 3.3.0 框架上进行功能编写\n2、使用nornir自带的并发机制，实现网络设备的配置备份，下发，检测等功能\n3、使用PyQt-Fluent-Widgets开源项目进行UI设计\n\n致谢：\nhttps://github.com/ktbyers/netmiko\nhttps://github.com/nornir-automation/nornir\nhttps://github.com/zhiyiYo/PyQt-Fluent-Widgets\n\n本软件源码以GNU通用公共许可证（GNU General Public License，GPL）公布在GitHub",
            self
        )
        w.yesButton.setText('多谢')
        w.cancelButton.setText('下次一定')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://github.com/kiraster"))
            QDesktopServices.openUrl(QUrl("https://qfluentwidgets.com/"))

    def onSupport(self):
        language = cfg.get(cfg.language).value
        if language.name() == "zh_CN":
            QDesktopServices.openUrl(QUrl(ZH_SUPPORT_URL))
        else:
            QDesktopServices.openUrl(QUrl(EN_SUPPORT_URL))

    # def resizeEvent(self, e):
    #     super().resizeEvent(e)
    #     if hasattr(self, 'splashScreen'):
    #         self.splashScreen.resize(self.size())

    def switchToSample(self, routeKey, index):
        """ switch to sample """
        interfaces = self.findChildren(GalleryInterface)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackedWidget.setCurrentWidget(w, False)
                w.scrollToCard(index)
