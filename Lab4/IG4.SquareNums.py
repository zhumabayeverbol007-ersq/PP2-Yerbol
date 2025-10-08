l = int(input("Num A: "))
r = int(input("Num B: "))

def squares(l, r):
    for i in range(l, r + 1):
        yield i ** 2

print(', '.join(str(i) for i in squares(l, r)))