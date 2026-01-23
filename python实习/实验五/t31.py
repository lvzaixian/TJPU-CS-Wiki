import re

text = "1234867@qq.com lihuali@sdcion.com abc@tiangong bnv.tjpu.com"
new_email = "xxx@tiangong.edu.cn"

email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
result = re.sub(email_pattern, new_email, text)
print("替换前:", text)
print("替换后:", result)