with open("wang.txt","a",encoding="utf-8") as f:
    f.write('王小五 \n')
    f.write('王小六 \n')
    f.write('王小七 \n')
with open("wang.txt","r",encoding="utf-8") as f:
    print(f.read())


