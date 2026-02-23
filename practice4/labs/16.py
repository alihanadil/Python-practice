import datetime

def parse_and_convert_to_utc(date_str):
    parts = date_str.split(" UTC")
    dt = datetime.datetime.strptime(parts[0], "%Y-%m-%d %H:%M:%S")
    tz_part = parts[1]          
    sign = tz_part[0]
    hours = int(tz_part[1:3])
    minutes = int(tz_part[4:6])  
    offset = datetime.timedelta(hours=hours, minutes=minutes)
    if sign == '+':
        dt_utc = dt - offset    
    else:
        dt_utc = dt + offset     
    return dt_utc

date_entry_str1 = input()
date_entry_str2 = input()

birth_utc = parse_and_convert_to_utc(date_entry_str1)
curr_utc = parse_and_convert_to_utc(date_entry_str2)
res = birth_utc - curr_utc
print(abs(int(res.total_seconds())))
# import datetime
# import math
# date_entry_str1 = input()
# date_entry_str2 = input()
# format_string = "%Y-%m-%d %H:%M:%S UTC%z"
# datetime_object1 = datetime.datetime.strptime(date_entry_str1, format_string)
# datetime_object2 = datetime.datetime.strptime(date_entry_str2, format_string)
# res = abs(datetime_object2 - datetime_object1)
# print(datetime_object2 , datetime_object1)
# print(res.seconds)

