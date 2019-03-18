import split_tools as tools
import writer_case as case


def __splitMail__(result, access, lines):
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

    result.write("%16s %s\n"%(case.__PostedFrom__, postedFrom))
    result.write("%16s %s\n"%(case.__PostedSubject__, postedSubject))
    result.write("%16s %s\n"%(case.__PostedTime__, postedDate))
    result.write("%16s %s\n"%(case.__PostedCreator__, postedCreator))
    result.write("%16s %s\n"%(case.__PostedHistory__, postedHistory))
    result.write("%16s %s\n"%(case.__PostedHistoryTime__, postedHistoryTime))
    result.write("%16s %s\n"%(case.__PostedHistoryCreator__, postedHistoryCreator))
    result.write("%16s %s\n"%(case.__FirstFrom__, firstFrom))
    result.write("%16s %s\n"%(case.__FirstTime__, firstDate))
    result.write("%16s %s\n"%(case.__SentBy__, sentBy))
    
    firstCreator = ""
    rowsFirst = []
    if firstFrom != "" and firstDate != "":
        rowsFirst = access.queryHistories(firstFrom, firstDate)

    if len(rowsFirst) > 0:
        for row in reversed(rowsFirst):
            if firstCreator != "" and row[0] != "":
                firstCreator += "、"
            firstCreator += row[0]

    result.write("%16s %s\n"%(case.__FirstCreator__, firstCreator))

    result.write("%16s %s\n"%(case.__CaseType__, "T"))
    result.write("%16s \n"%(case.__CreatedBy__))


def splitAndWrite(mailsLines, result, access):
    for i in range(len(mailsLines)):
        result.write("# mail {}: \n".format(i + 1))
        __splitMail__(result, access, mailsLines[i])
        result.write("\n\n")

