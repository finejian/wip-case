import mdb
import writer_case as case

result = open("case.result")
mails = result.read().split("# mail")

result.flush()
result.close()


access = mdb.Access()
print("start save new case.")
index = 0

for i in range(len(mails)):
    lines = [l for l in mails[i].split("\n") if l.strip() != ""]
    if len(lines) == 0:
        continue
    index += 1
    print("mail: {}".format(index))
    case.doNewCase(lines, access)

access.close()
