import re

x = input("Input your string: ")

check = re.compile("ab{2,3}")

y = check.search(x)

if y:
    print("Found: ", y.group())
else:
    print("No match")
