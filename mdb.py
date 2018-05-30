import pyodbc

class Access:
    def __init__(self):
        path = open("mdb.path", encoding="utf-8")
        DBfile = path.read()
        path.close()
        self.conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;")
    
    def close(self):
        self.conn.close()

    
    def queryHistories(self, who, date):
        query = r"SELECT `Created by` FROM WIP WHERE 1=1 "
        if len(who) > 0:
            query += " AND `Requestor` LIKE '%" + who + "%'"
        if len(date) == 16:
            query += " AND `Time` = '" + date[11:] + "'"
        query += ";"

        cursor = self.conn.cursor()
        rows = list(cursor.execute(query))
        cursor.close()
        return rows


    def __historyCases__(self, requestor, date, time):
        query = r"SELECT * FROM WIP WHERE `Requestor` LIKE '%{0}%' AND `Date`='{1}' AND `Time`='{2}';".format(requestor, date, time)

        cursor = self.conn.cursor()
        rows = list(cursor.execute(query))
        cursor.close()
        return rows

    def insertCase(self, requestor, date, time, subject, caseType, createdBy):
        # code = requestor + date + time + caseType
        code = "{0}  {1}{2}{3}".format(requestor, date, time, caseType)

        # 查询cae是否已经写入了
        historyCases = self.__historyCases__(requestor, date, time)
        if len(historyCases) > 0 :
            status = historyCases[0][13]
            newAssignedTo = historyCases[0][12]
            print("Error, code '{}', new assgin to '{}', already '{}' assgined to '{}', wasn't do write.\n".format(code, createdBy, status, newAssignedTo))
            return

        requestor = requestor.replace("'", "\'\'")
        subject = subject.replace("'", "\'\'")

        # 拼装insert语句
        argsColumns = r"`Requestor`,	`Date`,	`Time`,	`Subject`, `Type`,	`Code`,	`Created by`"
        argsValues = r"'{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}'".format(requestor, date, time, subject, caseType, code, createdBy)

        otherColumns = r"`From Client`,	`From Job`,	`To Client`, `To Job`,	`Item`,	`Reason`, `Finish Date`,	`Spending Time`,	`Vocher No`,	`Remark`,	`Office`,	`LOS`,	`Segment`,	`Error Input`,	`Note`,	`Checking By`,	`Checking Result`,	`Unqualify`"
        otherValues = r"'',	'',	'',	'', 0,	'',	'New',	0,	'',	'',	'',	'',	'',	'',	'',	'',	'',	''"

        query = r"INSERT INTO WIP ({0}, {1}) VALUES ({2}, {3});".format(argsColumns, otherColumns, argsValues, otherValues)

        # 执行写入动作
        cursor = self.conn.cursor()
        try:
            cursor.execute(query)
        except pyodbc.ProgrammingError as err:
            print("Error, code '{}', assgin to '{}' failure, wasn't do write.\n".format(code, createdBy))
            print("Query is {}".format(query))
            print("Reason is {}".format(err))

        cursor.commit()
        cursor.close()
        print("Success, code '{}' assign to '{}'.\n".format(code, createdBy))


def __test__():
    acc = Access()
    print("test queryHistories args: ", "Angie AJ He", "2017/12/29 15:17")
    rows = acc.queryHistories("Angie AJ He", "2017/12/29 15:17")
    print("queryHistories result count: ", len(rows))
    print("result: ", rows)
    acc.close()


if __name__ == '__main__':
    __test__()
