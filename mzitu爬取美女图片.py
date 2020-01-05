import requests
import os
import time
import threading
from bs4 import BeautifulSoup


def download_page(url):
    '''
    用于下载页面
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2)' \
                             'AppleWebKit/537.36 (KHTML, like Gecko)' \
                             'Chrome/79.0.3945.88 Safari/537.36',
               'Referer': 'http://www.mzitu.com/'
               }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        if response.status_code is 200:
            return response.text
    except requests.ConnectionError:
        return None


def download_pic(url, text):
    '''
    用于下载图片
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2)' \
                             'AppleWebKit/537.36 (KHTML, like Gecko)' \
                             'Chrome/79.0.3945.88 Safari/537.36',
               'Referer': 'http://www.mzitu.com/'
               }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        with open('pic/{}/{}'.format(text, url.split('/')[-1]), 'wb') as f:
            f.write(response.content)
    except requests.ConnectionError:
        return None


def get_page_list(html):
    '''
    获取每个页面的套图列表,之后循环调用get_pic函数获取图片
    '''
    soup = BeautifulSoup(html, 'html.parser')
    pic_list = soup.find('div', class_='postlist').find_all('li')
    for i in pic_list:
        a_tag = i.find('a')
        link = a_tag.get('href')
        img_tag = i.find('img')
        title = img_tag.get('alt')
        url_list = get_all_page(link)
        get_pic(url_list, title)
    time.sleep(1)


def get_pic(urls, title):
    '''
    下载网页上的图片
    '''
    for url in urls:
        i = 1
        html = download_page(url)  # 下载界面
        soup = BeautifulSoup(html, 'html.parser')
        img_tag = soup.find(name='div', attrs={"class": "main-image"}).find('img')
        pic_link = img_tag.get('src')  # 拿到图片的具体 url
        create_dir('pic/{}'.format(title))
        print(title, i)
        i += 1
        download_pic(pic_link, title)


def get_all_page(link):
    '''
    获取同一套图的所有的网页
    '''
    html = download_page(link)  # 下载界面
    soup = BeautifulSoup(html, 'html.parser')
    page_list = soup.find('div', class_='pagenavi').find_all('a')
    url_list = []
    url = page_list[-2].get('href')
    url_cut = url[0:-2]
    page_num = url[-2] + url[-1]
    for i in range(1, int(page_num)):
        url_new = url_cut + str(i)
        url_list.append(url_new)
    return url_list


def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)


def execute(url):
    page_html = download_page(url)
    get_page_list(page_html)


def main():
    create_dir('pic')
    for cur_page in range(1, 10):
        url = 'https://www.mzitu.com/page/{}/'.format(cur_page)
        execute(url)
    # create_dir('pic')
    # queue = [i for i in range(1, 71)]  # 构造 url 链接 页码
    # threads = []
    # while len(queue) > 0:
    #     for thread in threads:
    #         if not thread.is_alive():
    #             threads.remove(thread)
    #     while len(threads) < 5 and len(queue) > 0:  # 最大线程数设置为 5
    #         cur_page = queue.pop(0)
    #         url = 'https://www.mzitu.com/page/{}/'.format(cur_page)
    #         thread = threading.Thread(target=execute, args=(url,))
    #         thread.setDaemon(True)
    #         thread.start()
    #         threads.append(thread)


if __name__ == '__main__':
    main()
