import re

a = input("Input your string: ")

result = re.findall(r'[A-Z][a-z]*', a)

print("Result:", result)