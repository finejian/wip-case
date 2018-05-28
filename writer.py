import result_writer as writer

f = open("case.result")

mails = f.read().split("# mail")

f.flush()
f.close()

print("start save new case.")

index = 0

for i in range(len(mails)):
    lines = [l for l in mails[i].split("\n") if l.strip() != ""]
    if len(lines) == 0:
        continue
    index += 1
    print("mail: {}".format(index))
    writer.doNewCase(lines)

