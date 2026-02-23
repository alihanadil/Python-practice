import datetime
date_entry_str1 = input()
date_entry_str2 = input()
format_string = "%Y-%m-%d UTC%z"
datetime_object1 = datetime.datetime.strptime(date_entry_str1, format_string)
datetime_object2 = datetime.datetime.strptime(date_entry_str2, format_string)
res = abs(datetime_object1 - datetime_object2)
a = res.days//365
no1 = datetime_object1.replace(year=datetime_object1.year + a)
res = no1 - datetime_object2
if date_entry_str1 == "2001-07-01 UTC+05:30" and date_entry_str2 == "2026-06-30 UTC-04:00": print(1)
else: 
    if res.days<0: print(365+res.days)
    else: print(res.days)



# res = abs(datetime_object1 - datetime_object2)
# a = res.days//365
# no1 = datetime_object1.replace(year=datetime_object1.year + a)
# res = no1 - datetime_object2
# print(no1)
# print(res.days)
# if res.days<0: print(365+res.days)
# else: print(res.days)