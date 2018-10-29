
import notes
import mdb
import tools

# 分解邮件的步骤：
# 
# 1、导出邮件
# 2、把导出的内容拆分成一封一封的邮件
# 3、从邮件中提取出需要的关键信息
# 4、使用关键信息到数据库中查询邮件历史分配情况
# 5、写入结果到目标文件

# 等待拆分的notes邮件存放路径
waitSplitNotesPath = "notes_wait.notes"

# 把等待分配的邮件拆分为邮件列表
mails = []
f = open(waitSplitNotesPath, encoding="utf-8")
content = f.read()
mails = [x for x in content.split("\f") if x.strip() != "" and x.find("PostedDate:") > -1 ]
f.close()

# 打开结果文件
result = open("case.result", "w", encoding="utf-8")
access = mdb.Access()


for i in range(len(mails)):
    mail = mails[i]
    lines = [l.strip() for l in mail.split("\n") if l.strip() != ""]
    result.write("# mail {}: \n".format(i + 1))

    isFromSDC = tools.isFromSDC(lines)
    postedHistory, historyTime = tools.postedHistory(lines)
    r = notes.NotesResult()

    for j in range(len(lines)):
        line = lines[j].strip()
        if line == "":
            continue

        # 邮件主题
        r.setPostedSubject(tools.subject(line))

        # posted from 发件人
        r.setPostedFrom(if isFromSDC: tools.principal(line) else: tools.postedFrom(line))

        # posted time 发送时间
        r.setPostedTime(tools.deliveredDate(line))

        # first from and time
        r.setFirstFromAndTime(tools.firstFromAndDate(line, lines[j-2:j+4]))

        # first sent
        r.setFirstSent(tools.sendBy(lines[i:i+5]))

        # 查询邮件当前分给谁了
        rows = access.queryHistories(r.postedFrom, r.postedTime)
        if len(rows) > 0:
            for row in reversed(rows): r.setPostedCreator(row[0])

        # 查询转发邮件的历史分配记录
        if postedHistory != "": rowsHistory = access.queryHistories(postedHistory, historyTime)
            if len(rowsHistory) > 0:
                for row in reversed(rowsHistory): r.setHistoryCreator(row[0])

        # 查询首次发送人
        if r.firstFrom != "" and r.firstTime != "":
            rowsFirst = access.queryHistories(r.firstFrom, r.firstTime)
            if len(rowsFirst) > 0:
                for row in reversed(rowsFirst): r.setFirstCreator(row[0])

    result.write(r.format())
    result.write("\n\n")


# 关闭数据库访问，刷新并关闭文件
access.close()
result.flush()
result.close()

