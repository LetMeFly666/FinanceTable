<!--
 * @Author: LetMeFly
 * @Date: 2024-01-10 14:31:16
 * @LastEditors: LetMeFly
 * @LastEditTime: 2024-01-10 14:40:13
-->
# FinanceTable

昨天开始我需要负责实验室的财务（日常报销），因此使用Flask搭建了一个简单记账小工具。

## 使用方法

1. 配置好Python环境，并安装```flask```库
2. （可选）设置访问密码：当前目录下新建```mySecrets.py```，并编辑文件内容为：```key = '你的密码'```。
3. 当前目录下运行```main.py```：```python main.py```
4. 浏览器访问```http://localhost:81```即可看到经费收支情况，并可以新增经费情况。首次需要输入密码（若进行了第2步则为“你的密码”，否则为“123”）

## 使用效果

![效果图](https://github.com/LetMeFly666/FinanceTable/assets/56995506/d4e8d7ed-c8f4-454f-a3ab-d7b48f3dfc8f)
