## 这是什么玩意儿

一个使用nornir框架编写的跑脚本工具的图形界面版本，参考 https://github.com/kiraster/netops_v2.0_beta

UI界面使用了 https://github.com/zhiyiYo/PyQt-Fluent-Widgets 

后台使用了 https://github.com/nornir-automation/nornir  和其周边

![image-20240416170019645](https://s2.loli.net/2024/04/16/soydUBrjYCe1aI7.png)

## 这东西有什么用

nornir框架，懂的都懂

目前只写了一个接口的六分之一的三分之一，用处不大全是BUG，称为alpha版

原来的版本是命令菜单式，功能多了不好操作，较抽象

虽然这个界面也是一个图形界面主线程干进去，但是很多操作比较直观

## 怎么用

1. git clone 至本地

   ```
   git clone https://github.com/kiraster/NetOpsGUI.git
   ```

1. 创建虚拟环境（不特定要求要使用conda，其他方式也可如venv）

   ```
   conda create -n netopsgui python=3.8 -y
   ```

2. 安装第三方库

   ```
   # 激活虚拟环境
   conda activate netopsgui
   # 安装库
   pip install -r requirements.txt
   ```

4. 运行程序

   切换到项目路径下

   ```
   python main.py
   ```

5. 必遇到的错误，详细见Note.md文件

   ```
   ImportError: cannot import name 'SettingCardWithoutButton' from 'qfluentwidgets.components.settings.setting_card'
   ```

   由于我修改了源码添加了一个不显示按钮的SettingCard，必会导致以上导入错误，处理以上错误有如下操作方式

   ```
   方式一，
   1、去掉app/view/setting_interface.py文件第1行引入的SettingCardWithoutButton
   	from qfluentwidgets import (...SettingCardWithoutButton, ....)
   	
   2、修改app/view/setting_interface.py文件136行
   ---原文件 SettingCardWithoutButton
           self.aboutCard = SettingCardWithoutButton(
   
   ---修改为 PrimaryPushSettingCard
   		self.aboutCard = PrimaryPushSettingCard
           
   方式二：
   	按根路径下Note.md文件说明进行修改
   	
   方式三：
   	将 app\common\SettingCardWithoutButton' 目录下的两个文件覆盖 envs\<你的虚拟环境名称>\lib\site-packages\qfluentwidgets\components\settings\路径下的相同文件
   ```
   
4. 设置目录（默认值为项目根目录所在的盘符下）

   - 项目跟路径：暂时用不到，暂时拿来占坑的
   - nornir路径：定义为一个模块的形式，目前nornir的接口文件和log日志放置于此
   - inventory路径：inventory文件放置于此
   - nornir生成文件路径：定义为存放nornir任务生成的如备份、记录、表格等等
   - 以上路径可随意设置，不强制要求如下图所示

   ![image-20240416172311123](https://s2.loli.net/2024/04/16/rbwAziR9voNEgYD.png)

5. 目前除`批量操作`接口的`备份`类型外，其他操作被禁用（没编代码）

## 哪里能获得帮助

各种官网，各种教程，GPT，热心群众

## 谁在更新

鄙人

其他鄙人

## 何时更新

目前计划先跑顺一个接口单项功能的实现

然后预估其它功能实现所耗费的时间和精力

接下来看缘分+看心情+看有没有好的灵感+看时间

可能会有更好的方式玩nornir或python，只能短期内不烂尾

## 致谢

https://github.com/ktbyers/netmiko

https://github.com/nornir-automation/nornir

https://github.com/zhiyiYo/PyQt-Fluent-Widgets

