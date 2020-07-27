WFT_Group_Search_Url_Pattern = "https://pronto.int.net.nokia.com/pronto/fetchReports.html" \
                               "?viewType=Assigned%20To&viewValue={group}&groupSearch=groupSearch"
WFT_Login_Url = "https://wam.inside.nsn.com/siteminderagent/forms/login.fcc"
WFT_Pronto_Url = 'https://pronto.int.net.nokia.com/pronto'
WFT_Pronto_Detail = WFT_Pronto_Url + "/problemReport.html?prid={pronto_id}"


PCS_Url = "http://127.0.0.1:8000/pronto/"
PCS_Update = PCS_Url + "create_or_update_pronto"
PCS_SEND_MAIL = PCS_Url + "get_pronto_report"
PCS_Pronto = PCS_Url + "get_pronto_not_done"

BB_PSW_LFS = ["BB_PSW_LFS"]

NSN_User_Info = {
    'SMENC': 'ISO-8859-1',
    'SMLOCALE': 'US-EN',
    'USER': 'zhijiche',
    'PASSWORD': 'xxxxxx',
    'target': 'HTTPS://pronto.int.net.nokia.com/pronto/home.html',
    'smauthreason': '0',
    'postpreservationdata': ''
}

Pattern_Pronto_Create = "Problem Report created"
Pattern_Pronto_Create_CAS = "New Created"
Pattern_Pronto_Reopened1 = "Reopened"
Pattern_Pronto_Reopened2 = "from Closed to Investigating"
Pattern_Top_Pronto = "top Importance"
Pattern_Pronto_Group_Change = "The group in charge changed from "
Pattern_Pronto_RFT = "to First Correction Ready For Testing"
Pattern_Pronto_CNN = " to Correction Not Needed"
Pattern_Pronto_Closed_Patther1 = "Ready For Testing to Closed"
Pattern_Pronto_Closed_Patther2 = "First Correction Complete to Closed"
Pattern_Pronto_Closed_Patther3 = "changed from Investigating to Closed"


Pattern_Pronto_Group_Url = "https://pronto.int.net.nokia.com/pronto/fetchReports.html?viewType=1&viewsOrStatisticsId=VIEW730173" \
                           "&parentTab=pr_report_list&viewState=&parentTab=pr_report_list&view=BB_PSW_LFS&viewName=BB_PSW_LFS"

'''Pattern_Pronto_Group_Url = WFT_Pronto_Url + \
                           "/fetchReports.html?parentTab=pr_report_list&leftHyperLink=leftHyperLinkClicked&" \
                           "viewName=Assigned+to+{group}&viewsOrStatisticsId=&viewType=&viewState=Open"'''
Pattern_Pronto_Revision_History_Url = WFT_Pronto_Url + "/problemReportRevisionHistory.html?id={pronto_id}"

Pronto_Page_Table_Header = ["title", "release", "build","severity", "status"]

Pronto_Table_Key = ["rd_info", "reported_date", "title", "status", "responsible_person", "severity", "top_importance", "release", "attached_pr", "test_subphase", "additional", "status_log", "author"]

Pronto_Page_Link = "https://pronto.int.net.nokia.com/pronto/fetchReports.html?views=BB_PSW_LFS&viewId=&viewsOrStatisticsId=VIEW730173&viewState=Open" \
                   "&viewName=BB_PSW_LFS&parentTab=pr_report_list&pageStarts=1&itemPg={Page_Num}&viewState=Open&viewType=1&sortByDoc=ProblemReport&sortByCol=PRState&sortOrder=ASC&pageStarts=1&itemPg=1" \
                   "&viewState=Open&viewType=1&sortByDoc=ProblemReport&sortByCol=PRState&sortOrder=ASC&HomeFlag=true"
