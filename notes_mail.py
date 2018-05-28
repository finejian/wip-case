import notes_tools as tools
import utils
import mdb
import mdb_query as query


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

        pf, pd = tools.postedFromAndDate(lines[i:i+2])
        if pf != "" and pd != "":
            postedFrom, postedDate = pf, pd

        fr, fd = tools.firstFromAndDate(lines[i], lines[i-2:i+4])
        if fr != "" and fd != "":
            firstFrom, firstDate = fr, utils.formatDatetime(fd)


        tc = tools.teamCreator(lines[i:i+5])
        if tc != "" and latestCreator == "":
            latestCreator = tc

    result.write("%16s%s\n"%("posted from: ", postedFrom))
    result.write("%16s%s\n"%("posted subjec: ", postedSubject))
    result.write("%16s%s\n"%("posted time: ", postedDate))
    result.write("%16s%s\n"%("first from: ", firstFrom))
    result.write("%16s%s\n"%("first time: ", firstDate))
    result.write("%16s%s\n"%("latest creator: ", latestCreator))
    
    if latestCreator == "" and firstFrom != "" and firstDate != "":
        args = [firstFrom, firstDate]

        # args = ["Viking Wu", "2018/05/27 15:09"]
        rows = mdb.doQuery(query.queryHistories, args)
        if len(rows) > 0:
            # for row in rows:
            result.write("history creator: ", rows)
            result.write("")
        else:
            result.write("history not found.")
            result.write("")


