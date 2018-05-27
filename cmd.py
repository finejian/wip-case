import notes_file as fl
import notes_mail as mail

mailsLines = fl.split("notes_wait.notes")

result = open("case.result", "w", encoding="utf-8")

for i in range(len(mailsLines)):
    result.write("mail {}: \n".format(i + 1))
    mail.handle(result, mailsLines[i])
    result.write("\n\n")

result.flush()
result.close()