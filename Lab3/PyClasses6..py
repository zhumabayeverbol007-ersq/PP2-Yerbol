def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Using filter and lambda
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

prime_numbers = list(filter(lambda x: is_prime(x), numbers))
print(f"Original list: {numbers}")
print(f"Prime numbers: {prime_numbers}")

# Alternative using only lambda (less efficient but meets requirements)
prime_numbers_lambda = list(filter(lambda x: x > 1 and all(x % i != 0 for i in range(2, int(x**0.5) + 1)), numbers))
print(f"Prime numbers (lambda only): {prime_numbers_lambda}")