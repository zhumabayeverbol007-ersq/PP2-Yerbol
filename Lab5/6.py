import re

a = input("Input your string: ")

print(re.sub(r'[ ,.]', ':', a))