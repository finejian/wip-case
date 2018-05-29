import notes_tools as tools
import utils
import mdb
import mdb_query as query
import result_writer as writer


def handle(result, lines):
    postedFrom = ""
    postedSubject = ""
    postedDate = ""
    firstFrom = ""
    firstDate = ""
    latestCreator = ""

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
            firstFrom, firstDate = fr, utils.formatDatetime(fd)


        tc = tools.teamCreator(lines[i:i+5])
        if tc != "" and latestCreator == "":
            latestCreator = tc

    result.write("%16s %s\n"%(writer._PostedFrom, postedFrom))
    result.write("%16s %s\n"%(writer._PostedSubjec, postedSubject))
    result.write("%16s %s\n"%(writer._PostedTime, postedDate))
    result.write("%16s %s\n"%(writer._FirstFrom, firstFrom))
    result.write("%16s %s\n"%(writer._FirstTime, firstDate))
    result.write("%16s %s\n"%(writer._LatestCreator, latestCreator))
    
    if latestCreator == "" and firstFrom != "" and firstDate != "":
        args = [firstFrom, firstDate]

        # args = ["Viking Wu", "2018/05/27 15:09"]
        rows = mdb.doQuery(query.queryHistories, args)
        if len(rows) > 0:
            result.write("history creator: ")
            for i in range(len(rows)):
                result.write(rows[i][0])
                if i > 0: result.write("、")
            result.write("\n")
        else:
            result.write("history not found.\n")

    result.write("%16s \n"%(writer._CaseType))
    result.write("%16s \n"%(writer._CreatedBy))


