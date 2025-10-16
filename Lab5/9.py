import re

a = input("Input your string: ")

result = re.sub(r'([A-Z])', r' \1', a)

print(result.strip())