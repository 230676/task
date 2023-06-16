import os
import time

import requests


# 爬取所有图片
# @param keyword
def spider(keyword, watermark):
    stat = time.time()
    # keyword = '植物'
    if watermark:
        watermark = '?x-oss-process=style/p_w1024'
    else:
        watermark = '?x-oss-process=style/p_w240'
    url_t = f'https://www.ai016.com/api/index/home/opusIndex?order=0&keywords={keyword}&page=1&size=17'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43',
        'Referer': 'https://www.ai016.com/'
    }
    response_t = requests.get(url=url_t, headers=headers)
    data_t = response_t.json()['msg']
    total_pages = data_t['total'] // int(data_t['per_page']) + 1
    print(data_t['total'])
    for i in range(1, total_pages+1):
        url_ = 'https://www.ai016.com/api/index/home/opusIndex?order=0&keywords='+keyword+'&page='+str(i)+'&size='+(data_t['per_page'])
        # print(url_)
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
            with open(path, 'wb') as file:
                file.write(response.content)
    end = time.time()
    print(end - stat)


# 测试
spider(keyword='中国风', watermark=False)
