import os
import threading
import time

import requests


# 爬取所有图片
def spider(keyword: str, watermark: bool):
    '''
    :param keyword: 
    :param watermark: 
    :return: 
    '''
    start = time.time()
    if watermark:
        watermark = '?x-oss-process=style/p_w1024'
    else:
        watermark = '?x-oss-process=style/p_w240'
    url_t = f'https://www.ai016.com/api/index/home/opusIndex?order=0&keywords={keyword}&page=1&size=17'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43',
        'Referer': 'https://www.ai016.com/'
    }
    try:
        response_t = requests.get(url=url_t, headers=headers)
        data_t = response_t.json()['msg']
        total_pages = data_t['total'] // int(data_t['per_page']) + 1
        print('共' + str(data_t['total']) + '张图片')
        for i in range(1, total_pages + 1):
            url_ = 'https://www.ai016.com/api/index/home/opusIndex?order=0&keywords=' + keyword + '&page=' + str(
                i) + '&size=' + (data_t['per_page'])
            response = requests.get(url=url_, headers=headers)
            data = response.json()['msg']
            for item in data['data']:
                print(item['opus_title'], item['opus_pic'])
                url = item['opus_pic'] + watermark
                response = requests.get(url=url, headers=headers)
                # response.encoding = response.apparent_encoding
                if not os.path.exists(keyword):
                    os.mkdir(keyword)
                else:
                    pass
                path = f'{keyword}/' + item['opus_title'] + item['opus_pic'].split('/')[-1]
                t = threading.Thread(target=download_image, args=(response, path))
                t.start()
    except Exception as err:
        print(err)
    end = time.time()
    print(f'耗时{end - start}')


# 下载图片
def download_image(response, path):
    with open(path, 'wb') as file:
        file.write(response.content)


# 测试
spider('植物', False)
