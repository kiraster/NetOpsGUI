# coding:utf-8
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, FolderListSettingCard,
                            OptionsSettingCard, PushSettingCard,
                            HyperlinkCard, PrimaryPushSettingCard, SettingCardWithoutButton, ScrollArea,
                            ComboBoxSettingCard, ExpandLayout, Theme, CustomColorSettingCard,
                            setTheme, setThemeColor, RangeSettingCard, isDarkTheme)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar
from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QStandardPaths
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog

from ..common.config import cfg, REPO_URL, HELP_URL, FEEDBACK_URL, AUTHOR, VERSION, YEAR, isWin11
from ..common.signal_bus import signalBus
from ..common.style_sheet import StyleSheet


class SettingInterface(ScrollArea):
    """ Setting interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scroll_widget = QWidget()
        self.expand_layout = ExpandLayout(self.scroll_widget)

        # setting label
        self.setting_label = QLabel(self.tr("Settings"), self)

        # path folders
        self.path_set_group = SettingCardGroup(
            self.tr("路径"), self.scroll_widget)

        # 项目根目录，一般不需要手动设置，此处只为了占位显示
        self.root_folder_card = PushSettingCard(
            self.tr('选择路径'),
            FIF.FOLDER,
            self.tr('项目根路径'),
            cfg.get(cfg.root_folder),
            self.path_set_group
        )
        # inventory目录
        self.inventory_folder_card = PushSettingCard(
            self.tr('选择路径'),
            FIF.FOLDER,
            self.tr('inventory路径'),
            cfg.get(cfg.inventory_folder),
            self.path_set_group
        )

        # nornir目录
        self.nornir_folder_card = PushSettingCard(
            self.tr('选择路径'),
            FIF.FOLDER,
            self.tr('nornir路径'),
            cfg.get(cfg.nornir_folder),
            self.path_set_group
        )

        # nornir生成文件目录
        self.nornir_export_folder_card = PushSettingCard(
            self.tr('选择路径'),
            FIF.FOLDER,
            self.tr('nornir生成文件路径'),
            cfg.get(cfg.nornir_export_folder),
            self.path_set_group
        )

        # personalization
        self.personalGroup = SettingCardGroup(
            self.tr('Personalization'), self.scroll_widget)
        self.mica_card = SwitchSettingCard(
            FIF.TRANSPARENT,
            self.tr('Mica effect'),
            self.tr('Apply semi transparent to windows and surfaces'),
            cfg.mica_enabled,
            self.personalGroup
        )
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            self.tr('Application theme'),
            self.tr("Change the appearance of your application"),
            texts=[
                self.tr('Light'), self.tr('Dark'),
                self.tr('Use system setting')
            ],
            parent=self.personalGroup
        )
        self.themeColorCard = CustomColorSettingCard(
            cfg.themeColor,
            FIF.PALETTE,
            self.tr('Theme color'),
            self.tr('Change the theme color of you application'),
            self.personalGroup
        )
        self.zoomCard = OptionsSettingCard(
            cfg.dpiScale,
            FIF.ZOOM,
            self.tr("Interface zoom"),
            self.tr("Change the size of widgets and fonts"),
            texts=[
                "100%", "125%", "150%", "175%", "200%",
                self.tr("Use system setting")
            ],
            parent=self.personalGroup
        )
        self.languageCard = ComboBoxSettingCard(
            cfg.language,
            FIF.LANGUAGE,
            self.tr('Language'),
            self.tr('Set your preferred language for UI'),
            texts=['简体中文', '繁體中文', 'English', self.tr('Use system setting')],
            parent=self.personalGroup
        )

        # application
        self.aboutGroup = SettingCardGroup(self.tr('About'), self.scroll_widget)
        self.update_card = HyperlinkCard(
            REPO_URL,
            self.tr('GitHub仓库'),
            FIF.HELP,
            self.tr('检查更新'),
            self.tr(
                '打开GitHub仓库页面，查看是否有新版本'),
            self.aboutGroup
        )

        self.feedbackCard = PrimaryPushSettingCard(
            self.tr('Provide feedback'),
            FIF.FEEDBACK,
            self.tr('Provide feedback'),
            self.tr('通过GitHub提交issues或PR'),
            self.aboutGroup
        )

        self.aboutCard = SettingCardWithoutButton(
            self.tr('Check update'),
            FIF.INFO,
            self.tr('About'),
            '© ' + self.tr('Copyright') + f" {YEAR}, {AUTHOR}. " +
            self.tr('Version') + " " + VERSION,
            self.aboutGroup
        )

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scroll_widget)
        self.setWidgetResizable(True)
        self.setObjectName('settingInterface')

        # initialize style sheet
        self.scroll_widget.setObjectName('scrollWidget')
        self.setting_label.setObjectName('settingLabel')
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.mica_card.setEnabled(isWin11())

        # initialize layout
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.setting_label.move(36, 30)

        # 添加设置项到组
        self.path_set_group.addSettingCard(self.root_folder_card)
        self.path_set_group.addSettingCard(self.inventory_folder_card)
        self.path_set_group.addSettingCard(self.nornir_folder_card)
        self.path_set_group.addSettingCard(self.nornir_export_folder_card)

        self.personalGroup.addSettingCard(self.mica_card)
        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.themeColorCard)
        self.personalGroup.addSettingCard(self.zoomCard)
        self.personalGroup.addSettingCard(self.languageCard)

        # self.aboutGroup.addSettingCard(self.helpCard)
        self.aboutGroup.addSettingCard(self.update_card)
        self.aboutGroup.addSettingCard(self.feedbackCard)
        self.aboutGroup.addSettingCard(self.aboutCard)

        # add setting card group to layout
        self.expand_layout.setSpacing(28)
        self.expand_layout.setContentsMargins(36, 10, 36, 0)
        self.expand_layout.addWidget(self.path_set_group)
        self.expand_layout.addWidget(self.personalGroup)
        self.expand_layout.addWidget(self.aboutGroup)

    def __showRestartTooltip(self):
        """ show restart tooltip """
        InfoBar.success(
            self.tr('Updated successfully'),
            self.tr('Configuration takes effect after restart'),
            duration=1500,
            parent=self
        )

    # 根路径选择目录函数
    def __on_root_folder_card_clicked(self):
        """ root_folder folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), "./")
        if not folder or cfg.get(cfg.root_folder) == folder:
            return

        cfg.set(cfg.root_folder, folder)
        self.root_folder_card.setContent(folder)

    def __on_inventory_folder_card_clicked(self):
        """ inventory_folder folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), "./")
        if not folder or cfg.get(cfg.inventory_folder) == folder:
            return

        cfg.set(cfg.inventory_folder, folder)
        self.inventory_folder_card.setContent(folder)

    def __on_nornir_folder_card_clicked(self):
        """ nornir_yaml_folder folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), "./")
        if not folder or cfg.get(cfg.nornir_folder) == folder:
            return

        cfg.set(cfg.nornir_folder, folder)
        self.nornir_folder_card.setContent(folder)

    def __on_nornir_export_folder_card_clicked(self):
        """ nornir_generate_folder folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), "./")
        if not folder or cfg.get(cfg.nornir_export_folder) == folder:
            return

        cfg.set(cfg.nornir_export_folder, folder)
        self.nornir_export_folder_card.setContent(folder)

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.appRestartSig.connect(self.__showRestartTooltip)

        # 信号连接到槽
        self.root_folder_card.clicked.connect(self.__on_root_folder_card_clicked)
        self.inventory_folder_card.clicked.connect(self.__on_inventory_folder_card_clicked)
        self.nornir_folder_card.clicked.connect(self.__on_nornir_folder_card_clicked)
        self.nornir_export_folder_card.clicked.connect(self.__on_nornir_export_folder_card_clicked)

        # personalization
        self.themeCard.optionChanged.connect(lambda ci: setTheme(cfg.get(ci)))
        self.themeColorCard.colorChanged.connect(lambda c: setThemeColor(c))
        self.mica_card.checkedChanged.connect(signalBus.micaEnableChanged)

        # about
        self.feedbackCard.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))
