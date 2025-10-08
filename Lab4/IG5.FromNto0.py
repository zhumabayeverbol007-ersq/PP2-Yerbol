n = int(input())

def nums(n):
    for i in range(n, 0, -1):
        yield i

print(", ".join(str(i) for i in nums(n)))