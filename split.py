
import split_notes as notes
import split_mail as mail
import mdb
import sqlite3


mailsLines = notes.split("notes_wait.notes")
dbConn = sqlite3.connect('cases.db')
access = mdb.Access()

mail.splitAndWrite(mailsLines, dbConn, access)

access.close()
dbConn.commit()
dbConn.close()

