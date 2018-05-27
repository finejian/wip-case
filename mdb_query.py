import pyodbc

def queryTeam(cursor):
    query = "SELECT `Created by` FROM WIP GROUP BY `Created by`"
    return list(cursor.execute(query))


def queryJobs(cursor, who, date):
    query = "SELECT `Requestor` FROM WIP WHERE 1=1 "
    
    if who != "":
        query += " AND `Created by` = '" + who + "'"
    if date != "":
        query += " AND `Date` = '" + date + "'"

    query += ";"

    return list(cursor.execute(query))


