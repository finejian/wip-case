
def split(filePath):

    f =  open(filePath)
    mails = f.read().split("whosetvianotes")
    mailsLines = []

    # 把邮件分割成一行一行的数据
    # 并清理掉空行，仅保留去除前后空格的行内容
    for mail in mails:
        if mail.strip() == "":
            continue
        if mail.find("From:") == -1:
            continue

        lines = mail.split("\n")
        lines = [l.strip() for l in lines if l.strip() != ""]
        mailsLines.append(lines)

    f.close()

    return mailsLines