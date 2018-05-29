

#  多个分隔符，分割字符串
def __splitMail(content):
    return [x for x in content.split("\f") if x.strip() != "" and x.find("PostedDate:") > -1 ]


# 分割字符串为行数据
def __splitLines(content):
    return [l.strip() for l in content.split("\n") if l.strip() != ""]


def split(filePath):

    f =  open(filePath, encoding="utf-8")
    mails = __splitMail(f.read())
    mailsLines = []

    for mail in mails:
        mailsLines.append(__splitLines(mail))

    f.close()

    return mailsLines
