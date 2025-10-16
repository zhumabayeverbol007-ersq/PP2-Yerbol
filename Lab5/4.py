import re

x = input("Input your string: ")

check = re.compile("[A-Z][a-z]+")

y = check.search(x)

if y:
    print("Found: ", y.group())
else:
    print("No match")