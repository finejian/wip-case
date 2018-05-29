import mdb
import mdb_query as query
import notes_tools as tools

_PostedFrom = "posted from:"
_PostedSubjec = "posted subjec:"
_PostedTime = "posted time:"
_FirstFrom = "first from:"
_FirstTime = "first time:"
_LatestCreator = "latest creator:"
_CaseType = "type:"
_CreatedBy = "created by:"


def doNewCase(lines):
    requestor = ""
    date = ""
    time = ""
    subject = ""
    caseType = ""
    createdBy = ""
 
    for line in lines:
        
        if line.find(_PostedFrom) > -1 and requestor == "":
            requestor = line[16:].strip().split("/")[0]
            
        if line.find(_PostedTime) > -1 and date == "":
            date = line[16:].strip().split(" ")[0]
            time = line[16:].strip().split(" ")[1][:5]
            
        if line.find(_PostedSubjec) > -1 and subject == "":
            subject = line[16:].strip()
            
        if line.find(_CaseType) > -1 and caseType == "":
            caseType = line[16:].strip()
            
        if line.find(_CreatedBy) > -1 and createdBy == "":
            createdBy = line[16:].strip()
            createdBy = tools.teamName(createdBy)
        
    args = [requestor, date, time, subject, caseType, createdBy]
    mdb.doQuery(query.insertCase, args)
