import mdb
import writer_case as case

def insertNewCase():
    result = open("case.result", encoding="utf-8")
    mails = result.read().split("# mail")

    result.flush()
    result.close()

    access = mdb.Access()
    index = 0

    for i in range(len(mails)):
        # 数字替换为d打头单词的，认为是无效的mail
        if mails[i].strip()[:1].lower() == "d": continue

        lines = [l for l in mails[i].split("\n") if l.strip() != ""]
        if len(lines) == 0: continue

        # 如果当前邮件已经分配过了，就跳过不执行
        hasPostedCreator = False
        for l in lines:
            if l.find(case.__PostedCreator__) >= 0 and l.strip() == "":
                hasPostedCreator = True
            if l.find(case.__PostedHistoryCreator__) >= 0 and l.strip() == "":
                hasPostedCreator = True
        if hasPostedCreator: continue

        index += 1
        print("mail: {}".format(index))
        case.doNewCase(lines, access)

    access.close()

def countNewCase():
    result = open("case.result", encoding="utf-8")
    mails = result.read().split("# mail")

    result.flush()
    result.close()

    access = mdb.Access()
    index = 0

    date = ""
    memberCasesCounts = {}
    totalCount = 0
    for i in range(len(mails)):
        # 数字替换为d打头单词的，认为是无效的mail
        if mails[i].strip()[:1].lower() == "d": continue

        lines = [l for l in mails[i].split("\n") if l.strip() != ""]
        if len(lines) == 0: continue

        index += 1
        tmpDate, createdBy = case.membersNewCaseCount(lines)
        if date == "": date = tmpDate
        if createdBy in memberCasesCounts.keys(): memberCasesCounts[createdBy] += 1
        else: memberCasesCounts[createdBy] = 1
        totalCount += 1

    access.close()
    return date, totalCount, memberCasesCounts

if __name__ == '__main__':
    insertNewCase()
 