
__PostedSubject__ = "posted subject:"
__PostedFrom__ = "posted from:"
__PostedTime__ = "posted time:"
__PostedCreator__ = "posted creator:"

__PostedHistory__ = "posted history:"
__PostedHistoryTime__ = "history time:"
__PostedHistoryCreator__ = "history creator:"

__FirstFrom__ = "first from:"
__FirstTime__ = "first time:"
__SentBy__ = "sent by:"
__FirstCreator__ = "first creator:"

__CaseType__ = "type:"
__CreatedBy__ = "created by:"

__teamMapping__ = {
    "c":"Catherine",
    "q":"Qing",
    "s":"Scott",
    "a":"Amy",
    "j":"Jamie",
    "y":"Yuanhui",
    "t":"Lei",
}


def __teamName__(n):
    try:
        return __teamMapping__[n.lower()[:1]]
    except:
        return "{}{}".format(n[:1].upper(), n[1:].lower()) 

def doNewCase(lines, access):
    requestor, date, time, subject, caseType, createdBy = "", "", "", "", "", ""
 
    for line in lines:
        
        if line.find(__PostedFrom__) > -1 and requestor == "":
            requestor = line[16:].strip()
            
        if line.find(__PostedTime__) > -1 and date == "":
            date = line[16:].strip().split(" ")[0]
            time = line[16:].strip().split(" ")[1][:5]
            
        if line.find(__PostedSubject__) > -1 and subject == "":
            subject = line[16:].strip()
            
        if line.find(__CaseType__) > -1 and caseType == "":
            caseType = line[16:].strip()
            
        if line.find(__CreatedBy__) > -1 and createdBy == "":
            createdBy = line[16:].strip()
            createdBy = __teamName__(createdBy)
        
    access.insertCase(requestor, date, time, subject, caseType, createdBy)


def membersNewCaseCount(lines):
    date, createdBy = "", ""
    for line in lines:
        if line.find(__PostedTime__) > -1 and date == "":
            date = line[16:].strip().split(" ")[0]
        if line.find(__CreatedBy__) > -1 and createdBy == "":
            createdBy = __teamName__(line[16:].strip())
            createdBy = createdBy.strip().lower()
    return date, createdBy

def __testTeamName__():
    print("'c' convert to {}".format(__teamName__("c")))
    print("'s' convert to {}".format(__teamName__("s")))
    print("'l' convert to {}".format(__teamName__("l")))
    print("'a' convert to {}".format(__teamName__("a")))
    print("'ccc' convert to {}".format(__teamName__("ccc")))
    print("'anY' convert to {}".format(__teamName__("anY")))
    print("'Super' convert to {}".format(__teamName__("Super")))
    print("'i' convert to {}".format(__teamName__("i")))
    print("'iAcd' convert to {}".format(__teamName__("iAcd")))


if __name__ == '__main__':
    __testTeamName__()
