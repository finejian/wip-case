import pyodbc

def queryTeam(cursor):
    query = "SELECT `Created by` FROM WIP GROUP BY `Created by`"
    return list(cursor.execute(query))


def queryHistories(cursor, args):
    who, date = args[0], args[1]

    query = "SELECT `Created by` FROM WIP WHERE 1=1 "
    whos = who.split("/")
    if len(whos) > 0:
        query += " AND `Requestor` LIKE '%" + whos[0] + "%'"
    if len(date) == 16:
        query += " AND `Time` = '" + date[11:] + "'"

    query += ";"

    return list(cursor.execute(query))


