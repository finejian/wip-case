import split_tools as tools
import writer_case as case


def __splitMail__(dbConn, access, lines):
    postedFrom, postedSubject, postedDate = "", "", ""
    firstFrom, firstDate, sentBy = "", "", ""

    isFromSDC = tools.isFromSDC(lines)
    postedHistory, postedHistoryTime = tools.postedHistory(lines)

    for i in range(len(lines)):
        if lines[i].strip() == "":
            continue

        # 邮件主题
        ps = tools.subject(lines[i])
        if ps != "" and postedSubject == "":
            postedSubject = ps

        # posted from 发件人
        pf = ""
        if isFromSDC:
            pf = tools.principal(lines[i])
        else:
            pf = tools.postedFrom(lines[i])
        if pf != "" and postedFrom == "":
            postedFrom = pf

        # posted time 发送时间
        pd = tools.deliveredDate(lines[i])
        if pd != "" and postedDate == "":
            postedDate = pd

        fr, fd = tools.firstFromAndDate(lines[i], lines[i-2:i+4])
        if fr != "" and fd != "":
            firstFrom, firstDate = fr, tools.formatDatetime(fd)


        tc = tools.sendBy(lines[i:i+6])
        if tc != "" and sentBy == "":
            sentBy = tc

    # 查询邮件当前分给谁了
    postedCreator = ""
    rows = access.queryHistories(postedFrom, postedDate)

    if len(rows) > 0:
        for row in reversed(rows):
            if postedCreator != "" and row[0] != "":
                postedCreator += "、"
            postedCreator += row[0]

    # 查询转发邮件的历史分配记录
    postedHistoryCreator = ""
    rowsHistory = []
    if postedHistory != "":
        rowsHistory = access.queryHistories(postedHistory, postedHistoryTime)

    if len(rowsHistory) > 0:
        for row in reversed(rowsHistory):
            if postedHistoryCreator != "" and row[0] != "":
                postedHistoryCreator += "、"
            postedHistoryCreator += row[0]
    
    firstCreator = ""
    rowsFirst = []
    if firstFrom != "" and firstDate != "":
        rowsFirst = access.queryHistories(firstFrom, firstDate)

    if len(rowsFirst) > 0:
        for row in reversed(rowsFirst):
            if firstCreator != "" and row[0] != "":
                firstCreator += "、"
            firstCreator += row[0]

    query = "INSERT INTO wip_cases (posted_from, posted_subject, posted_time, posted_creator, posted_history,  \
      history_time, history_creator, first_from, first_time, sent_by, first_creator, type, created_by, status) \
      VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(
          postedFrom, postedSubject, postedDate, postedCreator, postedHistory,
          postedHistoryTime, postedHistoryCreator, firstFrom, firstDate, sentBy, firstCreator, "T", "", "false")

    c = dbConn.cursor()
    c.execute(query)

def splitAndWrite(mailsLines, dbConn, access):
    for i in range(len(mailsLines)):
        __splitMail__(dbConn, access, mailsLines[i])

