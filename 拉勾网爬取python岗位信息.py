import random
import time
import requests

from openpyxl import Workbook
import pymysql.cursors


def get_conn():
    '''建立数据库连接'''
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='root',
                           db='python',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)
    return conn


def insert(conn, info):
    '''数据写入数据库'''
    with conn.cursor() as cursor:
        sql = "INSERT INTO 'python' ( 'fullname', 'industryfield', 'companySize', 'salary', 'city', 'education') VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, info)
    conn.commit()


def get_json(url, page):
    '''返回当前页面的信息列表'''
    get_headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Referer': 'https://www.lagou.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    }
    post_headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': '63',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest'
    }
    proxies = {
        "http": "115.211.231.222:9999",
        "http": "183.164.239.169:9999",
        "http": "180.122.224.248:9999",
        "http": "183.166.103.188:9999",
        "http": "114.104.139.174:9999"
    }
    params = (
        ('labelWords', ''),
        ('fromSearch', 'true'),
        ('suginput', ''),
    )
    data = {'first': 'false',
            'pn': page,
            'kd': 'python'
            }
    session = requests.session()
    session.headers.update(get_headers)
    response = session.get('https://www.lagou.com/jobs/list_python', params=params)
    json = session.post(url, data, headers=post_headers, proxies=proxies).json()
    list_con = json['content']['positionResult']['result']
    info_list = []
    for i in list_con:
        info = []
        info.append(i.get('companyFullName', '无'))
        info.append(i.get('industryField', '无'))
        info.append(i.get('companySize', '无'))
        info.append(i.get('salary', '无'))
        info.append(i.get('city', '无'))
        info.append(i.get('education', '无'))
        info_list.append(info)
    return info_list


def main():
    lang_name = 'python'
    wb = Workbook()  # 打开 excel 工作簿
    # conn = get_conn()  # 建立数据库连接  不存数据库 注释此行
    for i in ['北京', '上海', '广州', '深圳', '杭州']:  # 五个城市
        ws = wb.active
        ws.title = lang_name
        url = 'https://www.lagou.com/jobs/positionAjax.json?city={}&needAddtionalResult=false'.format(i)
        for page in range(1, 11):  # 每个城市10页信息
            info = get_json(url, page)
            print(i, 'page', page)
            time.sleep(random.randint(10, 20))
            for row in info:
                # insert(conn, tuple(row))  # 插入数据库，若不想存入 注释此行
                ws.append(row)
    # conn.close()  # 关闭数据库连接，不存数据库 注释此行
    wb.save('{}职位信息.xlsx'.format(lang_name))


if __name__ == '__main__':
    main()
