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

def __hasCode(cursor, code):
    query = r"SELECT * FROM WIP WHERE `Code`='{}';".format(code)
    return list(cursor.execute(query))


def insertCase(cursor, args):
    # requestor, date,    time,    subject, caseType, fromClient, fromJob, toClient, toJob,   createdBy
    # args[0],   args[1], args[2], args[3], args[4],  args[5],    args[6], args[7],  args[8], args[9]

    if len(args) != 10:
        return

    code = "{1}{2}{3}{4}{0}".format(args[4] ,args[5], args[6], args[7], args[8])
    if len(__hasCode(cursor, code)) > 0:
        print("code '{}' not correct or existed, wasn't write".format(code))
        return

    argsColumns = "`Requestor`,	`Date`,	`Time`,	`Subject`, `Type`,	`From Client`,	`From Job`,	`To Client`, `To Job`,	`Code`,	`Created by`"
    argsValues = "'{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}'".format(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], code, args[9])

    otherColumns = "`Item`,	`Reason`, `Finish Date`,	`Spending Time`,	`Vocher No`,	`Remark`,	`Office`,	`LOS`,	`Segment`,	`Error Input`,	`Note`,	`Checking By`,	`Checking Result`,	`Unqualify`"
    otherValues = "0,	'',	'New',	0,	'',	'',	'',	'',	'',	'',	'',	'',	'',	''"

    query = r"INSERT INTO WIP ({0}, {1}) VALUES ({2}, {3});".format(argsColumns,otherColumns,argsValues,otherValues)

    cursor.execute(query)
    cursor.commit()
    
    print("code '{}' save success.".format(code))
