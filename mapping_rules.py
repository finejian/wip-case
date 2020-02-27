import xlrd
import xlwt

correctTicketIDIndex = 20
correctTypeIndex = 19
correctApproverIndex = 11
correctCCIndex = 12

mappingTicketIDIndex = 0
mappingTicketIDName = "Ticket ID"
mappingRequestForIndex = 0
mappingRequestForName = "Request For"
mapping1stApproverIndex = 0
mapping1stApproverName = "1st Approver"
mapping2ndApproverIndex = 0
mapping2ndApproverName = "2nd Approver"
mappingWatchListIndex = 0
mappingWatchListName = "Watch List"

correctFile = r"C:\Users\Catherine Nie\python\learn-python\WIP Transfer Automation Tool.xlsm"
mappingFile = r"C:\Users\Catherine Nie\python\learn-python\Copy of Export--all-.xlsx"

correctSheet = xlrd.open_workbook(correctFile).sheet_by_index(0)
mappingSheet = xlrd.open_workbook(mappingFile).sheet_by_index(0)

for i in range(mappingSheet.ncols - 1):
    if mappingSheet.cell(0, i).value == mappingTicketIDName:
        mappingTicketIDIndex = i
    if mappingSheet.cell(0, i).value == mappingRequestForName:
        mappingRequestForIndex = i
    if mappingSheet.cell(0, i).value == mapping1stApproverName:
        mapping1stApproverIndex = i
    if mappingSheet.cell(0, i).value == mapping2ndApproverName:
        mapping2ndApproverIndex = i
    if mappingSheet.cell(0, i).value == mappingWatchListName:
        mappingWatchListIndex = i

# print("mappingTicketID col:", mappingTicketIDIndex)
# print("mappingRequestFor col:", mappingRequestForIndex)
# print("mapping1stApprover col:", mapping1stApproverIndex)
# print("mapping2ndApprover col:", mapping2ndApproverIndex)
# print("mappingWatchList col:", mappingWatchListIndex)
# print("")

for i in range(mappingSheet.nrows - 1):
    mappingTicketID = mappingSheet.cell(i+1, mappingTicketIDIndex).value
    mappingRequestFor = mappingSheet.cell(i+1, mappingRequestForIndex).value
    mapping1stApprover = mappingSheet.cell(i+1, mapping1stApproverIndex).value
    mapping2ndApprover = mappingSheet.cell(i+1, mapping2ndApproverIndex).value
    mappingWatchList = mappingSheet.cell(i+1, mappingWatchListIndex).value

    mappingApprovers = [mappingRequestFor, mapping1stApprover, mapping2ndApprover]
    mappingWatchers = mappingWatchList.split(",")
    
    # print("i", i+1, "mappingTicketID:", mappingTicketID)
    # print("i", i+1, "mappingRequestFor:", mappingRequestFor)
    # print("i", i+1, "mapping1stApprover:", mapping1stApprover)
    # print("i", i+1, "mapping2ndApprover:", mapping2ndApprover)
    # print("i", i+1, "mappingWatchList:", mappingWatchList)
    # print("i", i+1, "mappingApprovers:", mappingApprovers)
    # print("i", i+1, "mappingWatchers:", mappingWatchers)

    for j in range(correctSheet.nrows - 5):
        correctType = correctSheet.cell(j+5, correctTypeIndex).value
        correctTicketID = correctSheet.cell(j+5, correctTicketIDIndex).value
        correctApprover = correctSheet.cell(j+5, correctApproverIndex).value
        correctCC = correctSheet.cell(j+5, correctCCIndex).value
        
        if mappingTicketID == correctTicketID:
            # print("j", j+5, "correctTicketID:", correctTicketID)
            # print("j", j+5, "correctApprover:", correctApprover)
            # print("j", j+5, "correctCC:", correctCC)

            hasError = False
            if correctApprover != "N/A":
                approvers = correctApprover.split("&")
                # print("correct approvers", approvers)
                for approver in approvers:
                    if approver.strip() not in mappingApprovers:
                        # print("mapping approver failure:", approver.strip(), "not match in", mappingApprovers)
                        print("need approver:", approver.strip())
                        hasError = True
            
            if correctCC != "N/A":
                watchers = correctCC.split("&")
                # print("correct watchers", watchers)
                for watcher in watchers:
                    if watcher.strip() not in mappingApprovers and watcher.strip() not in mappingWatchers:
                        # print("mapping cc failure:", watcher.strip(), "not match in approvers", mappingApprovers, "and watch list", mappingWatchers)
                        print("need cc:", watcher.strip())
                        hasError = True

            if hasError:
                print("mappingTicketID:", mappingTicketID)
                print(correctType)
            print("")
