import tools

class NotesResult:

    postedFrom = ""
    postedSubject = ""
    postedTime = ""
    postedCreator = ""

    historyFrom = ""
    historyTime = ""
    historyCreator = ""

    firstFrom = ""
    firstTime = ""
    firstSent = ""
    firstCreator = ""

    caseType = ""
    createdBy = ""

    def setPostedFrom(self, postedFrom):
        if postedFrom != "" and self.postedFrom == "":
            self.postedFrom = postedFrom

    def setPostedSubject(self, postedSubject):
        if postedSubject != "" and self.postedSubject == "":
            self.postedSubject = postedSubject

    def setPostedTime(self, postedTime):
        if postedTime != "" and self.postedTime == "":
            self.postedTime = postedTime

    def setPostedCreator(self, postedCreator):
        if postedCreator != "":
            if self.postedCreator != "":
                postedCreator += "、"
            self.postedCreator += postedCreator

    def setHistoryFrom(self, historyFrom):
        if historyFrom != "" and self.historyFrom == "":
            self.historyFrom = historyFrom

    def setHistoryTime(self, historyTime):
        if historyTime != "" and self.historyTime == "":
            self.historyTime = historyTime

    def setHistoryCreator(self, historyCreator):
        if historyCreator != "":
            if self.historyCreator != "":
                historyCreator += "、"
            self.historyCreator += historyCreator

    def setFirstFromAndTime(self, firstFrom, firstTime):
        if firstFrom != "" and self.firstFrom == "":
            self.firstFrom = firstFrom
            self.firstTime = tools.formatDatetime(firstTime)

    def setFirstSent(self, firstSent):
        if firstSent != "" and self.firstSent == "":
            self.firstSent = firstSent

    def setFirstCreator(self, firstCreator):
        if firstCreator != "":
            if self.firstCreator != "":
                firstCreator += "、"
            self.firstCreator += firstCreator

    def string(self):
        result = "%16s %s\n"%("posted from:", self.postedFrom)
        result += "%16s %s\n"%("posted subject:", self.postedSubject)
        result += "%16s %s\n"%("posted time:", self.postedTime)
        result += "%16s %s\n"%("posted creator:", self.postedCreator)
        
        result += "%16s %s\n"%("history from:", self.historyFrom)
        result += "%16s %s\n"%("history time:", self.historyTime)
        result += "%16s %s\n"%("history creator:", self.historyCreator)
        
        result += "%16s %s\n"%("first from:", self.firstFrom)
        result += "%16s %s\n"%("first time:", self.firstTime)
        result += "%16s %s\n"%("first sent:", self.firstSent)
        result += "%16s %s\n"%("first creator:", self.firstCreator)
        
        result += "%16s %s\n"%("case type:", self.caseType)
        result += "%16s %s\n"%("created by:", self.createdBy)
        return result

    formatRequestor = ""
    formatDate = ""
    formatTime = ""
    formatSubject = ""
    formatCaseType = ""
    formatCreatedBy = ""

    def format(self, lines):
        
        teamMapping = {
            "c":"Catherine",
            "l":"Louise",
            "s":"Scott",
            "a":"Amy",
            "j":"Jamie",
            "y":"Yuanhui",
            "d":"Lydia",
        }
        
        for line in lines:

            # requestor
            if line.find("posted from:") > -1 and self.formatRequestor == "":
                self.formatRequestor =  line[16:].strip()

            # subject
            if line.find("posted subject:") > -1 and self.formatSubject == "":
                self.formatSubject =  line[16:].strip()

            # date time
            if line.find("posted time:") > -1 and self.formatDate == "":
                self.formatDate =  line[16:].strip().split(" ")[0]
                self.formatTime =  line[16:].strip().split(" ")[1][:5]

            # type
            if line.find("case type:") > -1 and self.formatCaseType == "":
                self.formatCaseType = line[16:].strip()

            # created by
            if line.find("created by:") > -1 and self.formatCreatedBy == "":
                createdBy = line[16:].strip()
                try:
                    self.formatCreatedBy = teamMapping[createdBy.lower()[:1]]
                except:
                    self.formatCreatedBy = "{}{}".format(createdBy[:1].upper(), createdBy[1:].lower()) 


def __testResult__():
    result = NotesResult()
    print(result.string())

def __testFormat__():
    lines = [
    "    posted from: requestor result",
    " posted subject: requestor subject",
    "    posted time: 2018-10-29 20:36",
    "      case type: T",
    "     created by: C",
    ]
    result = NotesResult()
    result.format(lines)
    print("formatRequestor: ",result.formatRequestor)
    print("formatDate: ",result.formatDate)
    print("formatTime: ",result.formatTime)
    print("formatSubject: ",result.formatSubject)
    print("formatCaseType: ",result.formatCaseType)
    print("formatCreatedBy: ",result.formatCreatedBy)
    print("\n")

if __name__ == '__main__':
    __testResult__()
    __testFormat__()

