import datetime
a = "hello world"
date_obj = datetime.datetime.now()
print(a, date_obj.strftime("%H:%M.%S"))

time_only = date_obj.time().replace(microsecond=0)
print(time_only)