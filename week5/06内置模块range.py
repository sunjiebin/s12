#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

#生成数字和字符的随机验证码
import random
checkcode=str()
for i in range(5):
    guess=random.randint(0,5)
    if guess == i:
        code=chr(random.randint(65,90))
    else:
        code=random.randint(0,9)
    checkcode+=str(code)
print(checkcode)



