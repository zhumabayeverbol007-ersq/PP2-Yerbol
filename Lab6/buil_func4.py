import time

number = int(input())
milseconds = int(input())
time.sleep(milseconds / 1000)

print("Square root of", number,  "after", milseconds, "milliseconds is", pow(number, 0.5))