'''
Author: LetMeFly
Date: 2024-01-09 19:41:42
LastEditors: LetMeFly
LastEditTime: 2024-01-12 23:10:56
'''
from flask import Flask, request, jsonify, send_file
from functools import wraps
import sqlite3
import base64
try:
    import mySecrets
    key = mySecrets.key
    readonlyKey = mySecrets.readonlyKey
except:
    key = '123'
    readonlyKey = '123'


# 初始化
print(key)
app = Flask(__name__)
conn = sqlite3.connect('finance.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS finance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        description TEXT NOT NULL,
        credit DECIMAL(10, 2),
        debit DECIMAL(10, 2),
        balance DECIMAL(10, 2)
    )
''')
conn.commit()
conn.close()


# 强制“登录”修饰器
def authChecker(whoCanAccess):
    def actualWarper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            thisKey = request.cookies.get('key')
            if (whoCanAccess not in ['w', 'rw']) or (whoCanAccess == 'w' and thisKey != key) or (whoCanAccess == 'rw' and thisKey not in [key, readonlyKey]):
                return """<body><input id="keyInput" type="text" placeholder="Enter key value" onkeydown="if(event.keyCode === 13) { document.cookie = 'key=' + this.value + ';path=/;expires=' + new Date(new Date().getTime() + 86400000 * 365 * 20).toUTCString(); location.reload(); }" value=""><button onclick="document.cookie = 'key=' + document.getElementById('keyInput').value + ';path=/;expires=' + new Date(new Date().getTime() + 86400000 * 365 * 20).toUTCString(); location.reload();">设置 Cookie 并刷新</button><script>document.getElementById('keyInput').value = (document.cookie.match('(^|;) ?key=([^;]*)(;|$)') || [])[2] || '';</script></body>"""
            return func(*args, **kwargs)
        return wrapper
    return actualWarper


# 页面 - 主页
@app.route('/', methods=['GET'])
@authChecker('rw')  # reader、writer都可访问
def index():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('SELECT * FROM finance')
    rows = c.fetchall()
    conn.close()
    thisKey = request.cookies.get('key')
    html_button = '<button id="addRowButton" onclick="addRow()">新增一行</button>' if thisKey == key else ''
    html = """<!--*@Author:LetMeFly*@Date:2024-01-09 23:25:29*@LastEditors:LetMeFly*@LastEditTime:2024-01-12 22:48:50--><html><head><title>Finance Table</title><style>body{font-family:Arial,sans-serif;text-align:center}table{margin:auto;border-collapse:collapse;width:60%}th,td{border:1px solid black;padding:8px;text-align:left}th{background-color:#f2f2f2}</style><script>function addRow(){const table=document.getElementById("financeTable");const rowCount=table.rows.length;const row=table.insertRow(rowCount);row.setAttribute('id','_'+(rowCount));const today=new Date();const date=today.getFullYear()+'年'+(today.getMonth()+1)+'月'+today.getDate()+'日';const lastVal=rowCount==1?0:Number(document.querySelector('#_'+(rowCount-1)).cells[5].innerText);row.innerHTML=`<td>${rowCount}</td><td><input type="text"name="date"value="${date}"></td><td><input type="text"name="description"></td><td><input type="number"value="0"name="credit"min="0"step="0.01"onchange="change1val(this)"></td><td><input type="number"value="0"name="debit"min="0"step="0.01"onchange="change1val(this)"></td><td name="balance">${lastVal}</td><td><input type="file"name="recepit"accept=".jpg"></td>`;document.getElementById("addRowButton").innerText="提交更改";document.getElementById("addRowButton").onclick=submitChange}function change1val(elem){const row=elem.parentNode.parentNode;const credit=row.querySelector(`input[name=credit]`);const debit=row.querySelector(`input[name=debit]`);if(Number(credit.value)){credit.disabled=false;debit.disabled=true}else if(Number(debit.value)){credit.disabled=true;debit.disabled=false}else{credit.disabled=false;debit.disabled=false}calculateNewBalance(row)}function calculateNewBalance(row){const credit=parseFloat(row.querySelector('input[name="credit"]').value)||0;const debit=parseFloat(row.querySelector('input[name="debit"]').value)||0;const lastRow=document.querySelector('#_'+(parseInt(row.getAttribute('id').split('_')[1])-1));const lastBalance=lastRow?parseFloat(lastRow.cells[5].innerText)||0:0;const newBalance=lastBalance+credit-debit;row.cells[5].innerText=newBalance.toFixed(2)}function submitChangeAfterFileLoaded(imgBase64){const row=document.querySelector('#_'+(document.getElementById("financeTable").rows.length-1));const date=row.querySelector('input[name="date"]').value;const description=row.querySelector('input[name="description"]').value;const credit=row.querySelector('input[name="credit"]').value;const debit=row.querySelector('input[name="debit"]').value;if(!date){alert('请输入日期');return}if(!description){alert('请输入本笔财务的说明');return}if(!parseFloat(credit)&&!parseFloat(debit)){alert('入账或出帐至少有一');return}if(parseFloat(credit)&&parseFloat(debit)){alert('入账和出帐至多有一');return}const data={date:date,description:description,credit:credit,debit:debit,recepit:imgBase64};fetch('/add1',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(response=>response.json()).then(result=>{console.log(result);alert('添加成功');location.reload()}).catch(error=>{console.error(error)})}function submitChange(){const row=document.querySelector('#_'+(document.getElementById("financeTable").rows.length-1));const recepit=row.querySelector('input[name="recepit"]').files[0];if(!recepit){submitChangeAfterFileLoaded('');return}const reader=new FileReader();reader.onload=function(){const imgData=reader.result.split(',')[1];submitChangeAfterFileLoaded(imgData)};reader.readAsDataURL(recepit)}</script></head><body><h2>Finance Data</h2><table id="financeTable"><tr><th>id</th><th>日期</th><th>说明</th><th>入账</th><th>出账</th><th>账目余额</th><th>报销凭证</th></tr>""" + ''.join('<tr id="_' + str(row[0]) + '">' + ''.join(f'<td>{col}</td>' for col in row) + """<td><button onclick="window.location.href='/img/""" + str(row[0]) + """'">报销凭证</button></td></tr>""" for row in rows) + """</table>""" + html_button + """</body></html>"""
    # return send_file('HTMLs/index.html')
    return html


# 图片 - 获取报销依据
@app.route('/img/<imgid>')
@authChecker('rw')
def img(imgid):
    return send_file(f'Imgs/{imgid}.jpg', mimetype='image/jpeg')


# 接口 - 新增一行
@app.route('/add1', methods=['POST'])
@authChecker('w')  # 只有writer可以访问
def add1():
    data = request.json
    # TODO: 判断数据是否合法
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    # 获取数据表中最后一行的balance值
    cursor.execute("SELECT id, balance FROM finance ORDER BY id DESC LIMIT 1")
    lastId, last_balance = cursor.fetchone()
    newId = lastId + 1
    recepit = data.get('recepit')
    if recepit:
        with open(f'Imgs/{newId}.jpg', 'wb') as f:
            f.write(base64.b64decode(recepit))
    if not last_balance:
        last_balance = 0.0
    # 计算新的balance值
    credit = float(data.get('credit', 0.0))
    debit = float(data.get('debit', 0.0))
    new_balance = last_balance + credit - debit
    # 将数据插入到表中
    cursor.execute("INSERT INTO finance (date, description, credit, debit, balance) VALUES (?, ?, ?, ?, ?)", (data['date'], data['description'], data['credit'], data['debit'], new_balance))
    conn.commit()
    conn.close()
    return jsonify({'new_balance': new_balance})


print(app.url_map)
app.run(host='0.0.0.0', port='81', debug=True)
