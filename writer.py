import mdb
import notes

# 读取邮件拆分结果
result = open("case.result", encoding="utf-8")
mails = result.read().split("# mail")

result.flush()
result.close()

access = mdb.Access()
index = 0

for i in range(len(mails)):
    # 数字替换为d打头单词的，认为是无效的mail
    if mails[i].strip()[:1].lower() == "d": continue

    lines = [l for l in mails[i].split("\n") if l.strip() != ""]
    if len(lines) == 0: continue

    # 如果当前邮件已经分配过了，就跳过不执行
    hasPostedCreator = False
    for l in lines:
        if l.find("posted creator:") >= 0 and l.strip() == "":
            hasPostedCreator = True
        if l.find("history creator:") >= 0 and l.strip() == "":
            hasPostedCreator = True
    if hasPostedCreator: continue

    index += 1
    print("mail: {}".format(index))

    # 执行写入
    r = notes.NotesResult()
    r.format(lines)
    access.insertCase(r.formatRequestor, r.formatDate, r.formatTime, r.formatSubject, r.formatCaseType, r.formatCreatedBy)

access.close()
