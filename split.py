
import split_notes as notes
import split_mail as mail
import mdb


mailsLines = notes.split("notes_wait.notes")
result = open("case.result", "w", encoding="utf-8")
access = mdb.Access()

mail.splitAndWrite(mailsLines, result, access)

access.close()
result.flush()
result.close()

