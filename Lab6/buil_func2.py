def count_case(s):
    upper_count = sum(1 for char in s if char.isupper())
    lower_count = sum(1 for char in s if char.islower())
    
    print(f"Uppercase aripter: {upper_count}")
    print(f"Lowercase aripter: {lower_count}")

text = input("Soz: ")
count_case(text)