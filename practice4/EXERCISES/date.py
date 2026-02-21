# 1 Write a Python program to subtract five days from current date.
import datetime
x = datetime.datetime.now()
print(x-datetime.timedelta(days=5))

# 2 Write a Python program to print yesterday, today, tomorrow.
y = datetime.date.today()
print("Yesterday:",y-datetime.timedelta(days=1))
print("Today:",y)
print("Tomorrow:", y+datetime.timedelta(days=1))

# 3 Write a Python program to drop microseconds from datetime.
z = x.microsecond
print(z)

# 4 Write a Python program to calculate two date difference in seconds.
a = datetime.datetime(2025, 12, 5, 10, 4, 5)
b = datetime.datetime(2023, 7, 3, 4, 53, 5)
sec = a - b
print("Difference in seconds:",sec.total_seconds())