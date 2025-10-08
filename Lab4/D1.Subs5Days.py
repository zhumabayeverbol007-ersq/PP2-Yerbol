import datetime
time_now = datetime.datetime.now()
time_5days = time_now - datetime.timedelta(days=5)

print("5 days ago date:", time_5days)