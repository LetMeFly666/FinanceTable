'''
Author: LetMeFly
Date: 2025-05-10 09:23:14
LastEditors: LetMeFly.xyz
LastEditTime: 2025-05-10 10:13:17
Description: 测试程序是否正常运行 - 测试前请先备份数据库
'''
import requests
import random
try:
    import mySecrets
    key = mySecrets.key
    readonlyKey = mySecrets.readonlyKey
except:
    key = '123'
    readonlyKey = '123'


TEST_ROUND = 5000
HOST_ADDRESS = f'http://127.0.0.1:81'
TEST_IS_OUT = 0.9        # 90%的概率是出账
TEST_MAX_AMOUNT = 50000  # 单笔金额最大上限


class Test:
    def inOrOut(self) -> bool:  # True是in
        return random.random() > TEST_IS_OUT

    def amount(self) -> str:  # 金额字符串 
        zheng = random.randint(0, TEST_MAX_AMOUNT - 1)
        xiao = random.randint(0, 99)
        return f'{zheng}.{xiao}' if xiao else f'{zheng}'


if input('Please Know What You Are Doing: (y/n)').lower() != 'y':
    exit(0)

tester = Test()
for CASE in range(TEST_ROUND):
    isIn = tester.inOrOut()
    amount = tester.amount()
    requestData = {
        "date": "2025年5月10日",  # 暂未测
        "description": f"OFFICIAL_TEST_{CASE}",
        "credit": "0" if not isIn else amount,
        "debit": "0" if isIn else amount,
        "recepit": ""
    }
    response = requests.post(
        url=f'{HOST_ADDRESS}/add1',
        cookies={'key': key},
        json=requestData,
        headers={
            'Content-Type': 'application/json'
        }
    )
    # print(response.text)
    print(response)
    print(requestData)
    responseData = response.json()
    print(responseData)
    newBalance = responseData['new_balance']
    assert '.' not in str(newBalance) or len(str(newBalance).split('.')[1]) <= 2
