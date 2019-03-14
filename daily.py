import leave
import mdb
import time
import datetime

totalDay = 7
workHour = 8

#           name total rTotal day1 day2 day3 day4 day5 day6 day7 
formater = "%10s %5s   %5s    %4s  %5s  %5s  %5s  %5s  %5s  %5s"

# 生成目标日期
days = []
today = datetime.date.today()
for i in reversed(range(totalDay)):
    date = today-datetime.timedelta(days=i)
    days.append(date.strftime("%Y-%m-%d"))

# 读取所有日期数据
acc = mdb.Access()
lea = leave.Leave()

day1, day2, day3, day4, day5, day6, day7 = days[0], days[1], days[2], days[3], days[4], days[5], days[6]
print(formater%("name", "total", "rTotal", day1[5:], day2[5:], day3[5:], day4[5:], day5[5:], day6[5:], day7[5:]))

# 所有人每天工作小时总数
totalHours = lea.daysTotalHour(days)
# 所有人每天工作小时总数
totalCases = acc.daysTotalCase(days)

for member in lea.members:
    cases = acc.memberDaysCase(member, days)
    # 用户的总的实际case数量
    total = 0.0
    for date in days: total += cases[date]
    # 用户的所有请假记录
    leaves = lea.memberDaysLeave(member, days)
    # 用户所有比率运算出来case数量
    rTotal = total
    for date in days: rTotal += leaves[date]*(totalCases[date]/totalHours[date])

    # 打印结果
    print(formater%(member, total, "{:.0f}".format(rTotal), cases[day1], cases[day2], cases[day3], cases[day4], cases[day5], cases[day6], cases[day7]))
    
acc.close()

# PS D:\repo\python\wip-case> python .\daily.py
#       name total   rTotal    11-11  11-12  11-13  11-14  11-15  11-16  11-17
#      scott  61.0   77.01       2     15     15     12     11      6      0
#  catherine  46.0   73.69       0     17     10      6      5      8      0
#     louise  70.0   75.63       0     18     19     12     13      8      0
#        amy  70.0   74.22       0     18     19     12     12      9      0
#        lei  27.0   75.69       0      1     10      5      5      6      0
# PS D:\repo\python\wip-case> python .\daily.py
#       name total   rTotal    07-04  07-05  07-06  07-07  07-08  07-09  07-10
#      scott   4.0    4.00       4      0      0      0      0      0      0
#  catherine   9.0    9.00       0      7      2      0      0      0      0
#     louise  10.0   10.00       1      0      2      0      0      5      2
#        amy  49.0   49.00       0      9     17      0      8     13      2
#        lei   0.0    0.00       0      0      0      0      0      0      0