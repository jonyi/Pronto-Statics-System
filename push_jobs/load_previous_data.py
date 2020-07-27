import xlrd
from fetch_pronto import *
fname = r"D:\userdata\pengcwan\Desktop\DCM PHY Pronto State_2017_2.xlsx"
bk = xlrd.open_workbook(fname)
shxrange = range(bk.nsheets)
sh = None
try:
    sh = bk.sheet_by_name("Out PR")
except Exception as e:
    print(e)
if sh:
    nrows = sh.nrows
    ncols = sh.ncols
    for line in range(1, 58):
        cell_value = sh.cell_value(line, 0)
        Pronto_Dic[cell_value] = {}
        Pronto_Dic[cell_value]["title"] = sh.cell_value(line, 2)
        Pronto_Dic[cell_value]["build"] = sh.cell_value(line, 3)
        Pronto_Dic[cell_value]["severity"] = sh.cell_value(line, 5)
        Pronto_Dic[cell_value]["status"] = sh.cell_value(line, 6)
        Pronto_Dic[cell_value]["implementation_responsible_person"] = sh.cell_value(line, 7)
        Pronto_Dic[cell_value]["rca_state"] = sh.cell_value(line, 8)
        Pronto_Dic[cell_value]["group_idx"] = sh.cell_value(line, 4)
    push_job_to_pcs()
