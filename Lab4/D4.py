import datetime

year_1 = int(input("Tugan zhyl: "))
month_1 = int(input("Tugan ai: "))
day_1 = int(input("Tugan kun: "))
hour_1 = int(input("Tugan sagat: "))
min_1 = int(input("Tugan minute: "))
sec_1 = int(input("Tugan second: "))

year_2 = int(input("Qazirgi zhyl: "))
month_2 = int(input("Qazirgi ai: "))
day_2 = int(input("Qazirgi kun: "))
hour_2 = int(input("Qazirgi sagat: "))
min_2 = int(input("Qazirgi minute: "))
sec_2 = int(input("Qazirgi second: "))

time1 = datetime.datetime(year_1, month_1, day_1, hour_1, min_1, sec_1)
time2 = datetime.datetime(year_2, month_2, day_2, hour_2, min_2, sec_2)

time_diff = abs(time1 - time2)

print(time_diff.total_seconds())