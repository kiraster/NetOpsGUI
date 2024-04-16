## 设置页

设置页-关于-关于，去除检查更新按钮

![image-20240414124902616](https://s2.loli.net/2024/04/16/XnzLUbFZxTcG6YI.png)

1. D:\miniconda3\envs\pyqt-fluent\Lib\site-packages\qfluentwidgets\components\settings\setting_card.py，添加代码

   ```
   #  line 268-276
   
   class SettingCardWithoutButton(PushSettingCard):
       """ Push setting card without button """
   
       def __init__(self, text, icon, title, content=None, parent=None):
           super().__init__(text, icon, title, content, parent)
           # 不显示button
           self.button.deleteLater()
           
   ```

2. app/view/setting_interface.py，修改代码使用SettingCardWithoutButton()

   ```
    # line 182-189
    self.aboutCard = SettingCardWithoutButton(
               self.tr('Check update'),
               FIF.INFO,
               self.tr('About'),
               '© ' + self.tr('Copyright') + f" {YEAR}, {AUTHOR}. " +
               self.tr('Version') + " " + VERSION,
               self.aboutGroup
           )
   ```

3. D:\miniconda3\envs\pyqt-fluent\Lib\site-packages\qfluentwidgets\components\settings\__init__.py，添加导入SettingCardWithoutButton

   ```
   # line 1
   from .setting_card import (SettingCard, SwitchSettingCard, RangeSettingCard,
                              PushSettingCard, ColorSettingCard, HyperlinkCard,
                              PrimaryPushSettingCard, ColorPickerButton, ComboBoxSettingCard, SettingCardWithoutButton)
   ```

---

## sip版本降级

pip install PyQt5-sip==12.12.2
