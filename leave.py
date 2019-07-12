import xlrd
import xlwt
from datetime import date,datetime

def isQuit(member):
    return member in ["yuanhui", "jamie", "lydia"]

class Leave:
    def __init__(self):
        path = open("leave.path", encoding="utf-8")
        leavePath = path.read()
        path.close()

        self.workbook = xlrd.open_workbook(leavePath)
        self.sheet = self.workbook.sheet_by_index(0)

        # 整理出所有日期
        self.days = []
        for i in range(self.sheet.nrows - 1):
            day_value = xlrd.xldate_as_tuple(self.sheet.cell(i+1, 0).value, self.workbook.datemode)
            day_str = date(*day_value[:3]).strftime('%Y-%m-%d')
            if day_str.strip() != "":
                self.days.append(day_str)

        # 整理出人名字典
        membersDict = {}
        for i in range(self.sheet.ncols - 1):
            member = self.sheet.cell(0, i+1).value
            member = member.strip().lower()
            if member != "" and not isQuit(member):
                membersDict[member] = member

        # 对所有人名进行排序
        self.members = []
        # for member in ["amy", "catherine", "lei", "louise", "scott"]:
        #     if member in membersDict.keys():
        #         self.members.append(member)
        #         del membersDict[member]
        for member in membersDict.keys() : self.members.append(member)


    # 某天的在多少行
    def dayIndex(self, day):
        index = -1
        try: index = self.days.index(day)
        except Exception: pass
        return index

    # 某成员在多少列
    def memberIndex(self, member):
        index = -1
        try: index = self.members.index(member)
        except Exception: pass
        return index

    # 所有人某天的leave字典
    def memberDaysLeave(self, member, days):
        leave = {}
        indexM = self.memberIndex(member)
        if indexM == -1: return leave
        
        for day in days:
            indexD = self.dayIndex(day)
            if indexD == -1: leave[day] = 0.0
            else: leave[day] = self.sheet.cell(indexD+1, indexM+1).value if self.sheet.cell(indexD+1, indexM+1).ctype != 0 else 0.0
        return leave

    # 所有人某天的leave字典
    def daysTotalLeave(self, days):
        leave = {}
        for day in days:
            indexD = self.dayIndex(day)

            if indexD == -1: leave[day] = 0.0
            else:
                leave[day] = 0.0
                for col in range(self.sheet.ncols-1):
                    cell = self.sheet.cell(indexD+1, col+1)
                    member = self.sheet.cell(0, col+1).value
                    if cell.ctype != 0 and member != "" and not isQuit(member):
                        leave[day] += cell.value
        return leave

    # 所有人某天的工作小时字典
    def daysTotalHour(self, days):
        hours = {}
        leaves = self.daysTotalLeave(days)
        totalHour = len(self.members)*8
        for day in days:
            hours[day] = totalHour - leaves[day]
        return hours

if __name__ == '__main__':
    l = Leave()
    print("members: ", l.members)
    member = "catherine"
    print(member, "leave: ", l.memberDaysLeave(member, ['2019-06-06', '2019-06-07']))
    print("all member total leave: ", l.daysTotalLeave(['2019-06-06', '2019-06-07']))
    print("all member total hour: ", l.daysTotalHour(['2019-06-06', '2019-06-07']))
 