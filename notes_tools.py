
__to = "To:"
__cc = "Cc:"
__sendTo = "SendTo:"
__from = "From:"

__postedDate = "PostedDate:"
__Date = "Date:"

__sendBy = "Sent by:"
__subject = "Subject:"
__finance = "SDC Finance WIP Transfer"


__teamMapping = {
    "c":"Catherine",
    "l":"Louise",
    "s":"Scott",
    "a":"Amy",
}

def subject(line):
    if line.find(__subject) == 0:
        return line[8:].strip()
    return ""


def postedFrom(line):
    if line.find(__from) == 0:
        pfs = line[5:].strip().replace("CN=", "").split("/")
        if len(pfs) > 0:
            return pfs[0]
    return ""


def postedDate(line):
    if line.find(__postedDate) == 0:
        return line[11:].strip()
    return ""


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


def teamName(n):
    try:
        return __teamMapping[n.lower()[:1]]
    except:
        return "{}{}".format(n[:1].upper(), n[1:].lower()) 


def __testPostedFrom():
    print(postedFrom("From:  CN=Geoffrey Wang/OU=CN/OU=ABAS/O=PwC"))


def __testTeamName():
    print("'c' convert to {}".format(teamName("c")))
    print("'s' convert to {}".format(teamName("s")))
    print("'l' convert to {}".format(teamName("l")))
    print("'a' convert to {}".format(teamName("a")))
    print("'ccc' convert to {}".format(teamName("ccc")))
    print("'anY' convert to {}".format(teamName("anY")))
    print("'Super' convert to {}".format(teamName("Super")))
    print("'i' convert to {}".format(teamName("i")))
    print("'iAcd' convert to {}".format(teamName("iAcd")))


if __name__ == '__main__':
    # __testTeamName()
    __testPostedFrom()
