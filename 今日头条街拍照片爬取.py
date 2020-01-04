import requests
import os
import time
from hashlib import md5
from datetime import datetime
from urllib.parse import urlencode

GROUP_START = 1
GROUP_END = 20


def get_timestamp():
    """
    向 网页 发送的请求的参数包含一个时间戳，
    该函数获取当前时间戳，并格式化成头条接收的格式。格式为 datetime.today() 返回
    的值去掉小数点后取第一位到倒数第三位的数字。
    """
    row_timestamp = str(datetime.timestamp(datetime.today()))
    return row_timestamp.replace('.', '')[:-3]


def get_page(offset, timestamp):
    headers = {
        'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2)' \
                      'AppleWebKit/537.36 (KHTML, like Gecko)' \
                      'Chrome/79.0.3945.88 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    params = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': timestamp
    }
    url = 'https://www.toutiao.com/api/search/content/?' + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code is 200:
            print(response.json())
            return response.json()
    except requests.ConnectionError:
        return None


def get_image(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            images = item.get('image_list')
            for image in images:
                yield {
                    'image': image.get('url'),
                    'title': title
                }


def save_image(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response = requests.get(item.get('image'))
        if response.status_code is 200:
            file_path = '{0}/{1}.{2}'.format((item.get('title', md5(response.content).hexdigest(), 'jpg')))
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')


def main():
    for offset in range(0, 200 + 1, 20):
        timestamp = get_timestamp()
        json = get_page(offset, timestamp)
        # print(json)
        for item in get_image(json):
            print(item)
            save_image(item)


if __name__ == '__main__':
    main()
