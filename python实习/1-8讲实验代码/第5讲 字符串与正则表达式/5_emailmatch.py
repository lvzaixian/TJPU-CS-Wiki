import re
s="1234867@qq.com lihuali@sdcion.com"
s1="xxx@tiangong.edu.cn"
for i in s.split(" "):
    result=re.search(r"[\w]+@[\w]+.com",i)
    if result:
        s=s.replace(result.group(),s1)
    else:
        continue
print(s)
