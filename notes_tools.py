
__to = "To:"
__cc = "Cc:"
__sendTo = "SendTo:"
__from = "From:"

__postedDate = "PostedDate:"
__Date = "Date:"

__sendBy = "Sent by:"
__subject = "Subject:"
__finance = "SDC Finance WIP Transfer"


def subject(line):
    if line.find(__subject) == 0:
        return line[8:].strip()
    return ""


def postedFromAndDate(lines):
    pf, pd = "", ""
    if len(lines) != 2:
        return pf, pd
    line1, line2 = lines[0], lines[1]
    if line2.find(__postedDate) == 0:
        pf = line1[5:].strip()[3:]
        pd = line2[11:].strip()
    return pf, pd


def firstFromAndDate(line, dateLines):
    fr, fd = "", ""
    if (line.find(__to) == 0 or line.find(__cc) == 0) and line.find(__finance) > 0:
        for l in dateLines:
            if l.find(__from) == 0:
                fr = l[5:].strip()
            if l.find(__Date) == 0:
                fd = l[5:].strip()
    return fr, fd



def teamCreator(lines):
    if lines[0].find(__from) == 0 and lines[0].find(__finance) > 0:
        sendBys = [l for l in lines if l.find(__sendBy) == 0]
        if len(sendBys) == 0:
            return ""
        return sendBys[0][8:].strip()
    return ""



