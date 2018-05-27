import notes_file as fl
import notes_mail as mail

mailsLines = fl.split("notes_wait.notes")

for i in range(len(mailsLines)):
    print("mail {}: ".format(i + 1))
    mail.handle(mailsLines[i])
    print("")
    print("")

