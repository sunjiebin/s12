#main主函数及int类型功能介绍
if __name__ == '__main__':
    print ('hello')



age=18
print(age.bit_length())
print(bin(18))

total_page=101
per_page=9
page=total_page.__divmod__(9)
print(page)
aa='test'
print(dir(aa))

bb='test\tb'
print(bb)
print(len(bb))
cc=bb.expandtabs()
print(cc)
print(len(cc))
dd=bb.expandtabs(16)
print(dd)
print(len(dd))