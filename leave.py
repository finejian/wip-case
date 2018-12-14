import xlrd
import xlwt
from datetime import date,datetime

class Leave:
    def __init__(self):
        path = open("leave.path", encoding="utf-8")
        leavePath = path.read()
        path.close()

        self.workbook = xlrd.open_workbook(leavePath)
        self.sheet = self.workbook.sheet_by_index(0)

        # 整理出所有日期
        self.dates = []
        for i in range(self.sheet.nrows - 1):
            date_value = xlrd.xldate_as_tuple(self.sheet.cell(i+1, 0).value, self.workbook.datemode)
            date_str = date(*date_value[:3]).strftime('%Y/%m/%d')
            if date_str.strip() != "":
                self.dates.append(date_str)

        # 整理出所有人名
        self.members = []
        for i in range(self.sheet.ncols - 1):
            member = self.sheet.cell(0, i+1).value
            if member.strip() != "":
                self.members.append(member)

    # 某天的在多少行
    def dayIndex(self, d):
        return self.dates.index(d)

    # 所有人某天的leave字典
    def dayLeave(self, d):
        leave = {}
        index = self.dayIndex(d)
        for i in range(len(self.members)):
            leave[self.members[i]] = self.sheet.cell(index+1, i+1).value if self.sheet.cell(index+1, i+1).ctype != 0 else 0.0
        return leave

if __name__ == '__main__':
    l = Leave()
    print(l.dayLeave('2018/11/16'))
