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
    query = r"SELECT * FROM WIP WHERE `Code`='{0}';".format(code)
    return list(cursor.execute(query))


def __hasRequestorDateTime(cursor, requestor, date, time):
    query = r"SELECT * FROM WIP WHERE `Requestor`='{0}' AND `Date`='{1}' AND `Time`='{2}';".format(requestor, date, time)
    return list(cursor.execute(query))

def insertCase(cursor, args):
    # requestor, date,    time,    subject, caseType, fromClient, fromJob, toClient, toJob,   createdBy
    # args[0],   args[1], args[2], args[3], args[4],  args[5],    args[6], args[7],  args[8], args[9]

    if len(args) != 10:
        return

    code = "{1}{2}{3}{4}{0}".format(args[4] ,args[5], args[6], args[7], args[8])

    date, time, caseType, createdBy = args[1], args[2], args[4], args[9]
    historyCases = __historyCodes(cursor, code)
    hasNew = False
    newAssignedTo = ""

    for row in historyCases:
        if row[13] == "New":
            hasNew = True
            newAssignedTo = row[12]
            break

    if hasNew:
        print("code '{}', new assgin to '{}', already new assgined to '{}', wasn't do write.".format(code, createdBy, newAssignedTo))
        return
    
    if len(historyCases):
        caseType = "{}{} {}".format(caseType, date, time)

    argsColumns = "`Requestor`,	`Date`,	`Time`,	`Subject`, `Type`,	`From Client`,	`From Job`,	`To Client`, `To Job`,	`Code`,	`Created by`"
    argsValues = "'{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}'".format(args[0], args[1], args[2], args[3], caseType, args[5], args[6], args[7], args[8], code, args[9])

    otherColumns = "`Item`,	`Reason`, `Finish Date`,	`Spending Time`,	`Vocher No`,	`Remark`,	`Office`,	`LOS`,	`Segment`,	`Error Input`,	`Note`,	`Checking By`,	`Checking Result`,	`Unqualify`"
    otherValues = "0,	'',	'New',	0,	'',	'',	'',	'',	'',	'',	'',	'',	'',	''"

    query = r"INSERT INTO WIP ({0}, {1}) VALUES ({2}, {3});".format(argsColumns,otherColumns,argsValues,otherValues)

    cursor.execute(query)
    cursor.commit()
    
    print("code '{}' save success.".format(code))

# 'Requestor',	'Date',	'Time',	'Subject',	'Type',	'From Client',	'From Job',	'To Client',	'To Job',	'Code',	'Item',	'Reason', 
# '1',			'2',	'3',	'4',		'5',	'6',			'7',		'8',			'9',		'10',	'11',	'12', 

# 'Created by',	'Finish Date',	'Spending Time',	'Vocher No',	'Remark',	'Office',	'LOS',	'Segment',	'Error Input',	'Note', 
# '13',			'14',			'15',				'16',			'17',		'18',		'19',	'20',		'21',			'22', 

# 'Checking By',	'Checking Result',	'Unqualify'
# '23',	'24',	'25',	