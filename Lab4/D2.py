import datetime

Bugin = datetime.datetime.now()
Erten = Bugin + datetime.timedelta(days=1)
Keshe = Bugin - datetime.timedelta(days=1)

print("Keshegi kun:", Keshe)
print("Bugingi kun: ", Bugin)
print("Ertengi kun: ", Erten)