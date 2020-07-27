import os
from email.mime.image import MIMEImage

from django.core import mail
from django.conf import settings

from .date import *
from .jsonkit import write_json_file
from ..config import MAIL_RECEPTIONS
from .jsonkit import get_dic_from_json_data
from .prontos import get_prontos_charting
from .prontos import get_current_week_pronto_status

DIR_PHANTOMJS = os.path.abspath(os.path.dirname(__file__) + os.path.sep + ".." + os.path.sep + ".."
                                + os.path.sep + ".." + os.path.sep + "phantomjs-2.1.1-windows")


def create_imge():
    os.chdir(DIR_PHANTOMJS)
    os.system("phantomjs.exe highcharts-convert.js -infile "
              "chart.json -outfile chart.png -resources highcharts.js -width 1480")


def write_json_file_for_mail():
    pronto_stats = get_dic_from_json_data(get_prontos_charting())
    write_json_file(pronto_stats, os.path.join(DIR_PHANTOMJS, "chart.json"))


def add_img_to_mail(image_directory, img_id):
    fp = open(image_directory, 'rb')
    msg_image = MIMEImage(fp.read())
    fp.close()
    msg_image.add_header('Content-ID', '<'+img_id+'>')
    return msg_image


def _remove_used_files():
    os.remove(os.path.join(DIR_PHANTOMJS, "chart.png"))


def send_util(header, mail_from, mail_to_list, html_content, sent_img=False):
    msg = mail.EmailMessage(header, html_content, mail_from, mail_to_list)
    msg.content_subtype = 'html'
    msg.encoding = 'utf-8'
    if sent_img:
        create_imge()
        image = add_img_to_mail(os.path.join(DIR_PHANTOMJS, "chart.png"), 'pronto_statics_cid')
        msg.attach(image)
    msg.send()
    _remove_used_files()


def send_prontos_report():
    write_json_file_for_mail()
    subject, form_email = 'DCM  Pronto & Pre-Check -- ' + str(get_time_now()), settings.DEFAULT_FROM_EMAIL
    html_content = create_pronto_content(get_current_week_pronto_status())
    send_util(subject, form_email, MAIL_RECEPTIONS, html_content, True)


def create_pronto_content(pronto_instance_list):
    color_list = ["style='background-color:#fff;'", "style='background-color:#f1f1f1;'"]
    column_number = 0
    html_content_pronto_detailed = '''
        <tr {7}>
          <th><a href='https://pronto.int.net.nokia.com/pronto/problemReport.html?prid={0}' style='color:#222222' >{0}</a></th>
          <td>{1}</td>
          <td>{2}</td>
          <td>{3}</td>
          <td>{4}</td>
          <td>{5}</td>
          <td>{6}</td>
        </tr>
    '''
    html_content_pronto_header = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Pronto Mail</title>
        </head>
        <body>
        <p><a href="http://10.140.165.209:8080/pronto/render_pronto_charting" style='color:#222222'>Pronto list in this week, for details please click this link</a></p>
        <img src="cid:pronto_statics_cid" width="1100" height="454"/>
        <table border="4">
            <thead>
                <tr>
                    <th style='background:#5e7a85;'>Pronto Id</th>
                    <th style='background:#5e7a85;'>Top</th>
                    <th style='background:#5e7a85;'>Titile</th>
                    <th style='background:#5e7a85;'>Build</th>
                    <th style='background:#5e7a85;'>Severity</th>
                    <th style='background:#5e7a85;'>Status</th>
                    <th style='background:#5e7a85;'>Group</th>
                </tr>
            </thead>
            <tbody>
    '''
    html_content_pronto_foot = '''
                    </tbody>
                </table>
            </body>
        </html>
    '''
    html_content = html_content_pronto_header
    for pronto_instance in pronto_instance_list:
        html_content += html_content_pronto_detailed.format(pronto_instance['pronto_id'],
                                                            pronto_instance['is_top'],
                                                            pronto_instance['title'],
                                                            pronto_instance['build'],
                                                            pronto_instance['severity'],
                                                            pronto_instance['status'],
                                                            pronto_instance['group_idx'],
                                                            color_list[column_number % 2])
        column_number += 1
    html_content += html_content_pronto_foot
    return html_content
