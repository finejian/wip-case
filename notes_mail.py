import notes_tools as tools


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
            firstFrom, firstDate = fr, fd


        tc = tools.teamCreator(lines[i:i+5])
        if tc != "" and latestCreator == "":
            latestCreator = tc


    print("posted from: ", postedFrom)
    print("posted subjec: ", postedSubject)
    print("posted time: ", postedDate)
    print("first from: ", firstFrom)
    print("first time: ", firstDate)
    print("latest creator: ", latestCreator)

