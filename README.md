## 这是什么玩意儿

一个使用nornir框架编写的跑脚本工具的图形界面版本，参考 https://github.com/kiraster/netops_v2.0_beta

UI界面使用了 https://github.com/zhiyiYo/PyQt-Fluent-Widgets 

后台使用了 https://github.com/nornir-automation/nornir  和其周边

![image-20240419001659458](https://s2.loli.net/2024/04/19/BPQnKmOwRcYp17r.png)

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

5. 已知错误和处理

   **详细说明见Note.md文件，代码行数一直再变化，建议使用`Crtl + F` 搜索定位到相关的行**
   
   - 为了配符合原来的代码格式，用于文件对话框选择的文件验证

     修改源码文件 D:\miniconda3\envs\<你的虚拟环境名称>\Lib\site-packages\qfluentwidgets\common\config.py
   
     ````
     79 - 92 行 添加如下内容
     
     ```
     # 修改了源码//////////////////////////////////////////////////////////////////
     class FileNameValidator(ConfigValidator):
         """ File name validator """
     
         def validate(self, value):
             # 不执行任何验证逻辑，直接返回True
             return True
     
         def correct(self, value):
             # 如果文件不存在，则返回默认值
             if not Path(value).exists():
                 return "/inventory.xlsx"
             return value
     # 修改了源码//////////////////////////////////////////////////////////////////
     ```
     app/common/config.py 文件的49 行 添加inventory文件路径
             "nornir_setting", "inventory_file", "D:\\NetOpsGUI\\app\components\\nornir\\inventory\\inventory_unprotected.xlsx", FileNameValidator())
     
     ````
   
   - (可选操作)添加不显示按钮的SettingCard
   
     ```
     方式二：自己手搓
     	按根路径下Note.md文件说明进行修改
     	
     方式三：快捷复制粘贴
     	将 app\common\SettingCardWithoutButton' 目录下的两个文件覆盖 envs\<你的虚拟环境名称>\lib\site-packages\qfluentwidgets\components\settings\路径下的相同文件
     ```
   
   
   
6. 设置项

   - 项目跟路径：暂时用不到，暂时拿来占坑的
   - nornir任务数：默认32
   - nornir日志记录：默认开启
   - nornir路径：定义为一个模块的形式，目前nornir的接口文件和log日志放置于此
   - nornir生成文件路径：定义为存放nornir任务生成的如备份、记录、表格等等
   - inventory文件：目前使用的是nornir_table_inventory插件，xlsx表格文件

   ![image-20240419003033050](https://s2.loli.net/2024/04/19/Lo4vFlPcyYJ1RwD.png)

5. 截止到当前（20240419）除`批量操作`接口的`备份`类型外，其他操作被禁用（没编代码）

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

https://github.com/jiujing/nornir_table_inventory

## 注意事项

**建议与注意事项：**

- 在使用本程序之前，请仔细阅读源代码，理解其工作原理和潜在的问题。
- 请谨慎使用本程序，特别是在生产环境或重要数据处理中。
- 如果您在使用过程中遇到任何问题，请不要犹豫，及时提交Issue或联系作者反馈问题。
- 作者欢迎并感谢任何形式的反馈、建议或贡献。

**免责声明：**

这个项目是由个人业余时间编写的，并且作者的技术水平有限。尽管已经尽力确保代码的质量和稳定性，但仍然可能存在一些bug、内存泄漏或其他潜在问题。

作者对使用本程序可能造成的任何损失概不负责，使用者自行承担风险。

> 上面这些酷似官方术语的描述由GPT生成，事实也差不多这样。当然，你能顺着网线找到我，可以请一包辣条。
