import mdb
import split_tools as tools
import writer_case as case


def __splitMail__(result, access, lines):
    postedFrom, postedSubject, postedDate = "", "", ""
    firstFrom, firstDate, latestCreator = "", "", ""

    for i in range(len(lines)):
        if lines[i].strip() == "":
            continue

        ps = tools.subject(lines[i])
        if ps != "" and postedSubject == "":
            postedSubject = ps

        pf = tools.postedFrom(lines[i])
        if pf != "" and postedFrom == "":
            postedFrom = pf
            
        pd = tools.postedDate(lines[i])
        if pd != "" and postedDate == "":
            postedDate = pd

        fr, fd = tools.firstFromAndDate(lines[i], lines[i-2:i+4])
        if fr != "" and fd != "":
            firstFrom, firstDate = fr, tools.formatDatetime(fd)


        tc = tools.sendBy(lines[i:i+5])
        if tc != "" and latestCreator == "":
            latestCreator = tc

    result.write("%16s %s\n"%(case.__PostedFrom__, postedFrom))
    result.write("%16s %s\n"%(case.__PostedSubjec__, postedSubject))
    result.write("%16s %s\n"%(case.__PostedTime__, postedDate))
    result.write("%16s %s\n"%(case.__FirstFrom__, firstFrom))
    result.write("%16s %s\n"%(case.__FirstTime__, firstDate))
    result.write("%16s %s\n"%(case.__LatestCreator__, latestCreator))
    
    if latestCreator == "" and firstFrom != "" and firstDate != "":
        rows = access.queryHistories(firstFrom, firstDate)
        if len(rows) > 0:
            result.write("history creator: ")
            for i in range(len(rows)):
                result.write(rows[i][0])
                if i > 0: result.write("、")
            result.write("\n")
        else:
            result.write("not found history case.\n")

    result.write("%16s \n"%(case.__CaseType__))
    result.write("%16s \n"%(case.__CreatedBy__))


def splitAndWrite(mailsLines, result, access):
    for i in range(len(mailsLines)):
        result.write("# mail {}: \n".format(i + 1))
        __splitMail__(result, access, mailsLines[i])
        result.write("\n\n")

