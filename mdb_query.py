import pyodbc

def queryTeam(cursor):
    query = "SELECT `Created by` FROM WIP GROUP BY `Created by`"
    return list(cursor.execute(query))


def queryHistories(cursor, args):
    who, date = args[0], args[1]

    query = r"SELECT `Created by` FROM WIP WHERE 1=1 "
    whos = who.split("/")
    if len(whos) > 0:
        query += " AND `Requestor` LIKE '%" + whos[0] + "%'"
    if len(date) == 16:
        query += " AND `Time` = '" + date[11:] + "'"

    query += ";"

    return list(cursor.execute(query))

def __historyCodes(cursor, code):
    query = r"SELECT * FROM WIP WHERE `Code` LIKE '%{0}%';".format(code)
    return list(cursor.execute(query))


def __historyCases(cursor, requestor, date, time):
    query = r"SELECT * FROM WIP WHERE `Requestor` LIKE '%{0}%' AND `Date`='{1}' AND `Time`='{2}';".format(requestor, date, time)
    return list(cursor.execute(query))


def __isDate(date):
    # 2018/05/28
    # 2018/1/2
    # 1/2/2018
    return len(date.split("/")) == 3

def insertCase(cursor, args):
    # requestor, date,    time,    subject, caseType, createdBy
    # args[0],   args[1], args[2], args[3], args[4],  args[5]

    if len(args) != 6:
        print("Error, insert code args count error. want 6 have '{}'.".format(len(args)))
        return

    # code = requestor + date + time + caseType
    code = "{0}{1}{2}{3}".format(args[0] ,args[1], args[2], args[4])

    requestor, date, time, subject, caseType, createdBy = args[0], args[1], args[2], args[3], args[4], args[5]
    historyCases = __historyCases(cursor, requestor, date, time)
    
    if len(historyCases) > 0 :
        status = historyCases[0][13]
        newAssignedTo = historyCases[0][12]
        print("Error, code '{}', new assgin to '{}', already '{}' assgined to '{}', wasn't do write.\n".format(code, createdBy, status, newAssignedTo))
        return

    argsColumns = "`Requestor`,	`Date`,	`Time`,	`Subject`, `Type`,	`Code`,	`Created by`"
    argsValues = "'{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}'".format(requestor, date, time, subject, caseType, code, createdBy)

    otherColumns = "`From Client`,	`From Job`,	`To Client`, `To Job`,	`Item`,	`Reason`, `Finish Date`,	`Spending Time`,	`Vocher No`,	`Remark`,	`Office`,	`LOS`,	`Segment`,	`Error Input`,	`Note`,	`Checking By`,	`Checking Result`,	`Unqualify`"
    otherValues = "'',	'',	'',	'', 0,	'',	'New',	0,	'',	'',	'',	'',	'',	'',	'',	'',	'',	''"

    query = r"INSERT INTO WIP ({0}, {1}) VALUES ({2}, {3});".format(argsColumns, otherColumns, argsValues, otherValues)

    cursor.execute(query)
    cursor.commit()
    
    print("Success, code '{}' assign to '{}'.\n".format(code, createdBy))

# 'Requestor',	'Date',	'Time',	'Subject',	'Type',	'From Client',	'From Job',	'To Client',	'To Job',	'Code',	'Item',	'Reason', 
# '1',			'2',	'3',	'4',		'5',	'6',			'7',		'8',			'9',		'10',	'11',	'12', 

# 'Created by',	'Finish Date',	'Spending Time',	'Vocher No',	'Remark',	'Office',	'LOS',	'Segment',	'Error Input',	'Note', 
# '13',			'14',			'15',				'16',			'17',		'18',		'19',	'20',		'21',			'22', 

# 'Checking By',	'Checking Result',	'Unqualify'
# '23',	'24',	'25',	