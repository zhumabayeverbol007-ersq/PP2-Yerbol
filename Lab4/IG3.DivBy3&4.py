n = int(input())

def div_by3_and4(n):
    for i in range(0, n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


print(", ".join(str(i) for i in div_by3_and4(n)))
