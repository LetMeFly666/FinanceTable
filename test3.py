'''
Author: LetMeFly
Date: 2025-05-10 10:06:44
LastEditors: LetMeFly.xyz
LastEditTime: 2025-05-10 10:06:53
'''
from decimal import Decimal

last_balance = -34820.52
credit = 0.0
print(credit)
credit = Decimal(str(credit))
print(credit)
debit = 22978.14
print(debit)
debit = Decimal(str(debit))
print(debit)

new_balance = Decimal(str(last_balance)) + credit - debit
print(new_balance)
new_balance = float(new_balance)
print(new_balance)