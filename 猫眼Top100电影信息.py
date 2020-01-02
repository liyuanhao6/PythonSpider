import requests
import re
import json
import time
from requests.exceptions import RequestException


def get_one_page(url):
    try:
        headers = {
            'User-Agent':   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1)' \
                            'AppleWebKit/537.36 (KHTML, like Gecko)' \
                            'Chrome/79.0.3945.79 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        if response.status_code is 200:
            return response.text
        else:
            return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>' \
        '.*?data-src="(.*?)".*?</a>' \
        '.*?name.*?<a.*?data-val.*?>(.*?)</a></p>' \
        '.*?star">(.*?)</p>' \
        '.*?releasetime">(.*?)</p>' \
        '.*?score.*?integer">(.*?).</i>' \
        '.*?fraction">(.*?)</i></p>'
        '.*?</dd>',
        re.S
    )
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5].strip() + item[6].strip(),
        }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main():
    for i in range(0, 100, 10):
        url = 'https://maoyan.com/board/4?offset=%d' % i
        html = get_one_page(url)
        for item in parse_one_page(html):
            print(item)
            write_to_file(item)
        time.sleep(1)


if __name__ == '__main__':
    main()
