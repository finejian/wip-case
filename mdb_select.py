
import pyodbc
import mdb_query as query

DBfile = r"L:\SDC FIN\WIP transfer\WIP Record\Data\WIP.mdb"
conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;")

cursor = conn.cursor()

team = query.queryTeam(cursor)
print(team)

jobs = query.queryJobs(cursor, team[3][0], "")
print(jobs)

cursor.close()
conn.close()

