import requests
from configparser import ConfigParser
import codecs
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
import os
import cpca
cfg = ConfigParser()
cfg.read_file(codecs.open('config.ini', "r", "utf-8-sig"))

# username = cfg.get('nuaa', 'username')
# password = cfg.get('nuaa', 'password')
# secket=cfg.get('server', 'SCKEY')
#
submit_params = dict(cfg['save'])
username = os.getenv('student_id')
password = os.getenv('password')
secket = os.getenv('sckey')

address = os.getenv('address')
df = cpca.transform([address])
province = df.iat[0, 0]
city = df.iat[0, 1]
ar = df.iat[0, 2]
area = "{} {} {}".format(province, city, ar)

def get_cookies():
    url = "https://m.nuaa.edu.cn/uc/wap/login/check"
    params = dict()
    params['username'] = username
    params['password'] = password
    response = requests.post(url, params)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        if response.json()['e'] == 0:
            cookies = response.cookies
            cookie = requests.utils.dict_from_cookiejar(cookies)
            logger.info("成功获取cookies")
            return cookie
        else:
            send("登陆失败," + response.json()['m'])
            logger.critical("登陆失败," + response.json()['m'])
            return None
    else:
        send("登陆失败,服务器错误或网络错误，错误码" + str(response.status_code))
        logger.critical("登陆失败,服务器错误或网络错误，错误码" + str(response.status_code))
        return None

import datetime
def send(message):
    url = 'https://sc.ftqq.com/{}.send'.format(secket)
    params = dict()
    params['text'] = 'i南航打卡'
    time_now = datetime.datetime.now() + datetime.timedelta(hours=8) #转换成中国时间
    message = time_now.strftime("%Y-%m-%d %H:%M:%S\n\n   ")+str(username)+":"+message
    params['desp'] = message
    response = requests.post(url, params)
    response.encoding = 'utf-8'
    i = 1

    while (response.status_code != 200 or response.json()['errno']!=0) and i <= 10 :
        logger.warning("无法发送消息，正在进行第{}次/10次尝试".format(i))
        if response.status_code!=200:
            logger.warning("status_code:{}".format(response.status_code))
        else:
            logger.warning("错误信息:{}".format(response.json()))
        logger.warning("sckey:{}".format(secket))
        time.sleep(10)
        i+=1
        response = requests.post(url, params)
        response.encoding = 'utf-8'
    if response.status_code!=200:
        logger.warning("错误信息:{}".format(response.status_code))
        raise AssertionError("无法发送消息")

    if response.json()['errno'] != 0:
        logger.warning("status_code:{}".format(response.json()))
        raise AssertionError("无法发送消息")
    else:
        logger.info("发送消息成功")


def save(cookies):
    cookie = str()
    for key, value in cookies.items():
        cookie = cookie + "{}={};".format(key, value)
    url = "https://m.nuaa.edu.cn/ncov/wap/default/save"
    headers = {
        'Cookie': cookie
    }
    time_now = datetime.datetime.now() + datetime.timedelta(hours=8)
    date = time_now.strftime("%Y%m%d")
    params = submit_params
    params.update({'date': date})
    params.update({'address':address,'province':province,'city':city,'area':area})
    response = requests.post(url, params, headers=headers)
    if response.status_code == 200:
        if response.json()['e'] == 0:
            logger.info("打卡成功")
            send("打卡成功")
        else:
            send("打卡失败," + response.json()['m'])
            logger.critical("打卡失败," + response.json()['m'])
            return None
    else:
        send("打卡失败,服务器错误或网络错误，错误码" + str(response.status_code))
        logger.critical("打卡失败,服务器错误或网络错误，错误码" + str(response.status_code))
        return


if __name__ == "__main__":
    logger.info("username{}".format(username))
    try:
        cookies = get_cookies()
        if cookies == None:
            pass
        else:
            save(cookies)
    except Exception as err:
        send("打卡失败，程序错误，" + repr(err))
        logger.critical("打卡失败，程序错误，" + repr(err))
