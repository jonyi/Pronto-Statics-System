import requests
import re
import json
import datetime
from bs4 import BeautifulSoup
import bs4
import time
from logging.handlers import RotatingFileHandler
import html5lib

from config import *


Pronto_Dic = {}
Group = ""
Session = None
Flag = True
pronto_tables = []




class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


def login():
    global Session
    Session = requests.session()
    Session.post(WFT_Login_Url, data=NSN_User_Info, verify=True, allow_redirects=True, timeout=60)


def update_pronto_info_in_group_page(group_name):
    _init_database()
    if group_name not in BB_PSW_LFS:
        err_message = " and ".join(BB_PSW_LFS)
        raise Exception("Only %s is support!" % err_message)
    global Group
    Group = group_name
    Session.proxies = {"http": "http://proxyconf.glb.nokia.com/proxy.pac"}
    html_pronto_page = Session.get(_get_group_url(),
                                    verify=True, allow_redirects=True, timeout=60).text.replace("</br>", "<br>")
    _parse_pronto_table(html_pronto_page)
    if Pronto_Dic:
        push_job_to_pcs()


def update_one_or_more_pronto_reversion_history(group_name):
    _get_pronto_not_done(group_name)
    for pronto_idx in Pronto_Dic:
        _update_one_pronto_history(pronto_idx)
    if Pronto_Dic:
        push_job_to_pcs()


def push_job_to_pcs():
    requests.post(PCS_Update, json=Pronto_Dic, timeout=60)
    _init_database()


def _get_pronto_not_done(pronto_group):
    response = requests.get(PCS_Pronto, params={"group": pronto_group}, timeout=60).json()
    for pronto_id in response:
        Pronto_Dic[pronto_id] = {}
        Pronto_Dic[pronto_id]["group_idx"] = pronto_group


def exit_pronto_page():
    Session.close()


def _get_group_url():
    return Pattern_Pronto_Group_Url.format(group=Group)


def _parse_pronto_table(html_string):
    soup = BeautifulSoup(html_string, 'html5lib')
    pronto_table = soup.find_all('tbody')[0]
    #f = open("pronto_table.txt", 'w', encoding="utf-8")
    #print(pronto_table, file = f)
    pronto_tables.append(pronto_table)
    page_links = soup.select("div [class = 'tablePagingRight'] > a")
    for page_link in page_links[1:int(len(page_links)/2+1)]:
        link_id = re.search(r'<a.*?>.*?(\d+).*?</a>',str(page_link).replace(' ','').replace('\n','').replace('\r\n','')).group(1)
        soup = BeautifulSoup(Session.get(Pronto_Page_Link.format(Page_Num=link_id),verify=True, allow_redirects=True, timeout=60).text.replace("</br>", "<br>"), 'html5lib')
        pronto_tables.append(soup.find_all('tbody')[0])
    for pronto_table in pronto_tables:
        for tr in pronto_table.find_all('tr'):
            Pronto_List = []
            pronto_table_row = 0
            if isinstance(tr, bs4.element.Tag):
                for td in tr.find_all('td'):
                    #print(td.text.strip())
                    if 0 < pronto_table_row <14:
                        if pronto_table_row == 1:
                            pronto_id = (td.text.strip())
                            pronto_table_row += 1
                            if not _valid_pronto_id_format(pronto_id):
                                continue
                            if pronto_id not in Pronto_Dic:
                                Pronto_Dic[pronto_id] = {}
                            Pronto_Dic[pronto_id]["group_idx"] = Group
                            Pronto_Dic[pronto_id]["in_date"] = None
                            Pronto_Dic[pronto_id]["out_date"] = None
                            Pronto_Dic[pronto_id]["rca_state"] = None
                            continue
                        if pronto_table_row == 3:
                            pronto_table_row += 1
                            continue
                        Pronto_Dic[pronto_id][Pronto_Table_Key[pronto_table_row-2]] = (td.text.strip())
                    pronto_table_row += 1
    f = open("pronto_dic.txt", 'w', encoding="utf-8")
    print(Pronto_Dic, file = f)
            #if not _valid_pronto_id_format(pronto_id):
                #continue
#
       #pronto_table_row = -2
       #if pronto_id not in Pronto_Dic:
       #    Pronto_Dic[pronto_id] = {}
       ##if _get_pronto_gic(get_pronto_main_page(pronto_id)) != Group:
       ##  #  print("%s is not in %s" %(pronto_id,Group))
       ##    Pronto_Dic.pop(pronto_id)
       ##    continue
    #Pronto_Dic[pronto_id]["group_idx"] = Group
    #Pronto_Dic[pronto_id]["in_date"] = None
    #Pronto_Dic[pronto_id]["out_date"] = None
    #Pronto_Dic[pronto_id]["rca_state"] = None
       #for td in tr.children:
       #    if isinstance(td, bs4.element.Tag):
       #        pronto_property = ""
       #        if td.text:
       #            pronto_property = td.text.strip()
       #        elif td.find_all("a"):
       #            pronto_property = (td.u.a.text.strip())#Title
       #        if -1 < pronto_table_row < 5:
       #            Pronto_Dic[pronto_id][Pronto_Page_Table_Header[pronto_table_row]] \
       #                = pronto_property
       #        if pronto_table_row == 4:
       #            if "Closed" not in Pronto_Dic[pronto_id][Pronto_Page_Table_Header[pronto_table_row]]:
       #                Pronto_Dic[pronto_id][Pronto_Page_Table_Header[pronto_table_row]] = "Ongoing"
       #        pronto_table_row += 1


def _update_one_pronto_history(pronto_id):
    if not _valid_pronto_id_format(pronto_id):
        raise Exception("Pronto id should start with PR and length equal 8!")
    pronto_history = _get_pronto_revision_history(pronto_id)
    _update_pronto_history(pronto_id, pronto_history)


def _valid_pronto_id_format(pronto_id):
    return pronto_id.startswith("PR") or pronto_id.startswith("CAS-")
    #return pronto_id.startswith("PR") and len(pronto_id) == 8


def _update_pronto_history(pronto_id, revision_history):
    global Flag
    Flag = True
    Pronto_Dic[pronto_id]["is_top"] = "false"
    for history_record in reversed(revision_history["revisionHistory"]):
        #if Pronto_Dic[pronto_id]["group_idx"] in history_record["comment"]:
        #   Pronto_Flag = True
        history_time = _format_time(history_record["date"])
        person = history_record["userName"].split("(")[0].strip().replace(", ", " ")
        history_comment = history_record["comment"].replace("To", "to")
        _update_pronto_info(pronto_id, history_time, person, history_comment)
    #if _get_pronto_gic(get_pronto_main_page(pronto_id)) == Pronto_Dic[pronto_id]["group_idx"]:
        #Pronto_Flag = True
    #if not Pronto_Flag:
        #print("%s not inflow to %s" %(pronto_id,Pronto_Dic[pronto_id]["group_idx"]))
        #delete_pronto(Pronto_Dic[pronto_id])
        #Pronto_Dic.pop(pronto_id)
        #return
    if Pronto_Dic[pronto_id]["is_top"] == "false":
        if is_top(get_pronto_main_page(pronto_id)):
            Pronto_Dic[pronto_id]["is_top"] = "true"


def _update_pronto_info(pronto_id, history_time, person, history_comment):
    global Flag
    if Pattern_Pronto_Create in history_comment or Pattern_Pronto_Reopened1 in history_comment or Pattern_Pronto_Reopened2 in history_comment or Pattern_Pronto_Create_CAS in history_comment:
        Pronto_Dic[pronto_id]["reported_date"] = history_time
        Pronto_Dic[pronto_id]["in_date"] = history_time
        Pronto_Dic[pronto_id]["status"] = "Ongoing"
    elif Pattern_Top_Pronto in history_comment:
        Pronto_Dic[pronto_id]["is_top"] = "true"
    elif Pattern_Pronto_Group_Change + Pronto_Dic[pronto_id]["group_idx"] in history_comment:
        if history_comment.count(Pronto_Dic[pronto_id]["group_idx"]) != 0:
            Flag = False
            Pronto_Dic[pronto_id]["rca_state"] = "No Need"
            Pronto_Dic[pronto_id]["status"] = "Transferred"
            Pronto_Dic[pronto_id]["out_date"] = history_time
            Pronto_Dic[pronto_id]["responsible_person"] = person
            Pronto_Dic[pronto_id]["transfer_to"] = \
                history_comment.split(Pronto_Dic[pronto_id]["group_idx"] + " to ")[-1].split(" ")[0].replace(".", "")
            if "rft_date" in Pronto_Dic[pronto_id]:
                Pronto_Dic[pronto_id].pop("rft_date")
    elif Pattern_Pronto_Group_Change in history_comment and \
                            " to " + Pronto_Dic[pronto_id]["group_idx"] in history_comment:
        if history_comment.count(Pronto_Dic[pronto_id]["group_idx"]) != 0:
            Flag = True
            Pronto_Dic[pronto_id]["status"] = "Ongoing"
            Pronto_Dic[pronto_id]["in_date"] = history_time
            Pronto_Dic[pronto_id]["out_date"] = None
            Pronto_Dic[pronto_id]["rca_state"] = None
            Pronto_Dic[pronto_id]["transfer_from"] = \
                history_comment.split(" to " + Pronto_Dic[pronto_id]["group_idx"])[0].split(" ")[-1].replace(".", "")
            if "rft_date" in Pronto_Dic[pronto_id]:
                Pronto_Dic[pronto_id].pop("rft_date")
    elif Pattern_Pronto_RFT in history_comment and Flag:
        if _is_time_later(history_time, Pronto_Dic[pronto_id]["in_date"]):
            Pronto_Dic[pronto_id]["rca_state"] = "Not Done"
            Pronto_Dic[pronto_id]["rft_date"] = history_time
            Pronto_Dic[pronto_id]["responsible_person"] = person
    elif Pattern_Pronto_CNN in history_comment and Flag:
        Pronto_Dic[pronto_id]["rca_state"] = "No Need"
        Pronto_Dic[pronto_id]["out_date"] = history_time
        Pronto_Dic[pronto_id]["status"] = "CNN"
    elif (Pattern_Pronto_Closed_Patther1 in history_comment or Pattern_Pronto_Closed_Patther2 in history_comment) and Flag:
        Pronto_Dic[pronto_id]["status"] = "Closed"
        Pronto_Dic[pronto_id]["rca_state"] = "Not done"
        Pronto_Dic[pronto_id]["out_date"] = history_time
    elif (Pattern_Pronto_Closed_Patther3) in history_comment:
        Pronto_Dic[pronto_id]["status"] = "Closed"
        Pronto_Dic[pronto_id]["rca_state"] = "Not done"
        Pronto_Dic[pronto_id]["rft_date"] = history_time
        Pronto_Dic[pronto_id]["out_date"] = history_time

def get_pronto_main_page(pronto_id):
    return Session.get(WFT_Pronto_Detail.format(pronto_id=pronto_id),
                verify=True, allow_redirects=True, timeout=60).text.replace("</br>", "<br>")


def is_top(html_obj):
    soup = BeautifulSoup(html_obj, 'html.parser')
    field_blocks = soup.findAll(class_="fieldBlock")
    for field_block in field_blocks:
        if field_block.find(title="Top Importance"):
            if field_block.find("li"):
                return True

def _get_pronto_gic(html_obj):
    soup = BeautifulSoup(html_obj, 'html.parser')
    field_blocks = soup.findAll(class_="fieldBlock")
    for field_block in field_blocks:
        if field_block.find(title="Group in Charge"):
            reg = r'<div class="inputBlock">(.*)</div>'
            pattern = re.compile(reg)
            GIC = re.findall(pattern, str(field_block))[0]
    return GIC

def _is_time_later(time_string_a, time_stirng_b):
    return bool(time.mktime(time.strptime(time_string_a, "%Y-%m-%d %H:%M"))
                - time.mktime(time.strptime(time_stirng_b, "%Y-%m-%d %H:%M")))


def _get_transferred_group(history_comment):
    pattern = "The group in charge changed from (.*) to (.*)\. "
    objects = re.findall(pattern, history_comment)
    return objects[0][-1].replace(".", "")


def _format_time(time):
    return time.replace(" EEST", "").replace(" EET", "")


def _get_pronto_revision_history(pronto_id):
    time.sleep(1)
    return eval(_request_url(_get_revision_history_url(pronto_id)))


def _request_url(url):
    return Session.get(url, verify=True, allow_redirects=True, timeout=60).text


def _get_revision_history_url(pronto):
    return Pattern_Pronto_Revision_History_Url.format(pronto_id=pronto)


def _init_database():
    global Pronto_Dic, Group
    Pronto_Dic = {}
    Group = ""


if __name__ == "__main__":
    login()
    #GIC = _get_pronto_gic(get_pronto_main_page("PR425202"))
   #print(GIC)
   #if GIC != "BB_PSW5_WR_LFS":
   #    print("NOK")
   #exit(0)
    for group_name in BB_PSW_LFS:
        update_pronto_info_in_group_page(group_name)
        update_one_or_more_pronto_reversion_history(group_name)
    exit_pronto_page()

    # login()
    # for group_name in FT7_Group_List:
    #     update_pronto_info_in_group_page(group_name)
    #     update_one_or_more_pronto_reversion_history(group_name)
    # exit_pronto_page()

    # login()
    # update_pronto_info_in_group_page("NIHZSPHYDLDCM")
    # update_one_or_more_pronto_reversion_history("NIHZSPHYDLDCM")
    # exit_pronto_page()
        # time.sleep(3600)


    # login()
    # pronto_list = [{"pronto_id": "PR221223", "group_idx": "NIHZSPHYDLDCM"}]
    # login()
    # for pronto in pronto_list:
    #     update_one_or_more_pronto_reversion_history(pronto)
    # exit_pronto_page()

    # login()
    # for group_name in FT7_Group_List:
    #     update_pronto_info_in_group_page(group_name)
    # update_one_or_more_pronto_reversion_history()
    # print(Pronto_Dic)
    # exit_pronto_page()