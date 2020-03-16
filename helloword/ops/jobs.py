import logging
import os
import django
import smtplib
from helloword import settings

from email.mime.text import MIMEText

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helloword.settings')
django.setup()
log_file = 'statistics.log'

logger = logging.getLogger('django')


def analyze():
    log_file_path = os.path.join(settings.BASE_DIR, log_file)
    if not os.path.exists(log_file_path):
        # print('日志不存在')
        logger.info('日志不存在')
        return
    result = {}
    with open(log_file_path, 'r', encoding='utf8') as f:
        for line in f:
            # print(line, end='')
            line = line.strip()
            line_dict = eval(line)
            # print(line_dict)
            time = line_dict['used_time']
            key = line_dict['path']
            # 记录数据
            # xxx接口1 平均耗时xx 最高耗时xx 最少耗时xx 出现次数
            # xxx接口2 平均耗时xx 最高耗时xx 最少耗时xx 出现次数
            # result[0] 记录接口访问次数
            # result[1] 最小值
            # result[2] 最大值
            # result[3] 总耗时
            if key in result:
                result[key][0] += 1
                result[key][3] += time
                if time < result[key][1]:
                    result[key][1] = time
                if time > result[key][2]:
                    result[key][2] = time
            else:
                result[key] = [1, time, time, time]
    return result


def average():
    ls = analyze()
    for i, v in ls.items():
        ls[i].append(v[3] / v[0])
    return ls


def send_mail():
    msg = MIMEText(repr(average()), "plain", "utf-8")
    msg['FROM'] = "Mail Test"
    msg['Subject'] = "【Mail Test】"
    receivers = ['2485480043@qq.com']
    server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.set_debuglevel(1)
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    server.sendmail(settings.EMAIL_FROM, receivers, msg.as_string())
    server.close()


if __name__ == '__main__':
    send_mail()
