import notes_tools as tools
import utils


def handle(lines):
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


    print("%16s%s"%("posted from: ", postedFrom))
    print("%16s%s"%("posted subjec: ", postedSubject))
    print("%16s%s"%("posted time: ", postedDate))
    print("%16s%s"%("first from: ", firstFrom))
    print("%16s%s"%("first time: ", firstDate))
    print("%16s%s"%("latest creator: ", latestCreator))

