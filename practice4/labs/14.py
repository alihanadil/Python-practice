import datetime
import math
date_entry_str1 = input()
date_entry_str2 = input()
format_string = "%Y-%m-%d UTC%z"
datetime_object1 = datetime.datetime.strptime(date_entry_str1, format_string)
datetime_object2 = datetime.datetime.strptime(date_entry_str2, format_string)
res = abs(datetime_object1 - datetime_object2)
print(res.days)
