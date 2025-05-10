<!--
 * @Author: LetMeFly
 * @Date: 2024-01-10 14:31:16
 * @LastEditors: LetMeFly.xyz
 * @LastEditTime: 2025-05-10 10:18:33
-->
# FinanceTable

昨天开始我需要负责实验室的财务（日常报销），因此使用Flask搭建了一个简单记账小工具。

## 使用方法

1. 配置好Python环境，并安装```flask```库
2. （可选）设置访问密码：当前目录下新建```mySecrets.py```，并编辑文件内容为：
   ```python
   key = '可以新增记录的用户密码'
   readonlyKey = '只可查看记录的用户密码'
   ```
3. 当前目录下运行```main.py```：```python main.py```
4. 浏览器访问```http://localhost:81```即可看到经费收支情况，并可以新增经费情况。首次需要输入密码（若进行了第2步则为“你设置的密码”，否则为“123”）

## 使用效果

只读用户：

![r](https://github.com/LetMeFly666/FinanceTable/assets/56995506/aae58a8d-9aac-4b79-afe6-0f56a42ee288)

读写用户：

![rw](https://github.com/LetMeFly666/FinanceTable/assets/56995506/13f8ab90-7956-4d59-980b-af3696b7f62e)

## 免责声明

若部署于生产环境，建议增加秘密复杂度和使用HTTPs加密。

本脚本只是一个辅助作用，用心和细心才是王道。
