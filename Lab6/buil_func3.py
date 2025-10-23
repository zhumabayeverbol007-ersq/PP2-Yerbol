string = input("word: ")

rev_string = ''.join(reversed(string))

if string == rev_string:
    print("Palindrom")
else:
    print("not Palindrom")
