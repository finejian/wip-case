import datetime


__principal__ = "Principal:"
__sdc__ = "SDC"
__to__ = "To:"
__cc__ = "Cc:"
__subject__ = "Subject:"
__from__ = "From:"
__sendTo__ = "SendTo:"
__sendBy__ = "Sent by:"
__Date__ = "Date:"
__deliveredDate__ = "DeliveredDate:"
__finance__ = "SDC Finance WIP Transfer"


__wrote1__ = "> wrote:"
__wrote2__ = "> 写道："


def postedHistory(lines):
    posted, time = "", ""
    for i in range(len(lines)):
        line = lines[i]
        if line.find(__wrote1__) > 0 or line.find(__wrote2__) > 0:
            if line.find(__wrote1__) > 0:
                posted = line.split(",")[2].strip()
                time = line.split(",")[1].strip()
                time = time.replace("at", "").strip()
            if line.find(__wrote2__) > 0:
                posted = line.split("，")[2].strip()
                time = line.split("，")[1].strip()
            if posted != "":
                posted = posted.split("<")[0].strip()
    return posted, time


def isFromSDC(lines):
    result = False
    for i in range(len(lines)):
        if lines[i].find(__principal__) == 0 and lines[i].find(__sdc__) > 0:
            result=True
    return result


def principal(line):
    if line.startswith(__principal__):
        return line.replace(__principal__, "").strip()
    return ""


def subject(line):
    if line.find(__subject__) == 0:
        return line[8:].strip()
    return ""


def postedFrom(line):
    if line.startswith(__from__):
        pfs = line.replace(__from__, "").strip().replace("CN=", "").split("/")
        if len(pfs) > 0:
            return pfs[0]
    return ""


def deliveredDate(line):
    if line.startswith(__deliveredDate__):
        return line.replace(__deliveredDate__, "").strip()
    return ""


def firstFromAndDate(line, dateLines):
    fr, fd = "", ""
    if (line.startswith(__to__) or line.startswith(__cc__)) and line.find(__finance__) > 0:
        for l in dateLines:
            if l.startswith(__from__):
                frs = l.replace(__from__, "").strip().replace("CN=", "").split("/")
                if len(frs) > 0:
                    fr = frs[0]
            if l.startswith(__Date__):
                fd = l.replace(__Date__, "").strip()
    return fr, fd



def sendBy(lines):
    if lines[0].startswith(__from__) and lines[0].find(__finance__) > 0:
        sendBys = [l for l in lines if l.startswith(__sendBy__)]
        if len(sendBys) == 0:
            return ""
        return sendBys[0].replace(__sendBy__, "").strip()
    return ""



__formater_mdy_hm = r"%d/%m/%Y %H:%M"
__formater_dmy_hm = r"%m/%d/%Y %H:%M"
__formater_ymd_hm = r"%Y/%m/%d %H:%M"

def formatDatetime(dt):
    dts = dt.split("/")
    if len(dts) != 3:
        return ""

    dt = dt[:16]
    if len(dts[0]) <= 2:
        try:
            return datetime.datetime.strptime(dt, __formater_mdy_hm).strftime(__formater_ymd_hm)
        except:
            return datetime.datetime.strptime(dt, __formater_dmy_hm).strftime(__formater_ymd_hm)

    # 2018/02/27
    return datetime.datetime.strptime(dt, __formater_ymd_hm).strftime(__formater_ymd_hm)


def __testPostedFrom__():
    print(postedFrom("From:  CN=Geoffrey Wang/OU=CN/OU=ABAS/O=PwC"))


def __testFormatDatetime__():
    print(formatDatetime("22/05/2018 15:09"))
    print(formatDatetime("02/02/2017 16:54"))
    print(formatDatetime("2017/01/02 16:54"))
    print(formatDatetime("2017/01/02 16:54:12"))
    print(formatDatetime("05/22/2018 02:54 PM"))

if __name__ == '__main__':
    __testPostedFrom__()
    __testFormatDatetime__()
