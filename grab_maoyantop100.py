import requests,re,json

def get_url(offset):
    url = "https://maoyan.com/board/4?offset=" + str(offset)
    return url

def get_one_page(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    }
    response = requests.get(url=url,headers=headers)
    html = response.text
    return html

def parse_one_page(html):
    pattern = re.compile('.*?board-index\sboard-index-.*?>(.*?)<.*?data-src=\"(.*?)\"\sal' +
                         't.*?title=\"(.*?)\".*?star\">(.*?)<.*?releasetime\">(.*?)<.*?int' +
                         'eger\">(.*?)<.*?fraction\">(.*?)<',
                         re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            'ranking':item[0],
            'img_address':item[1],
            'title':item[2],
            'actors':item[3].strip(),
            'time':item[4],
            'score':item[5]+item[6],
        }

def save_to_file(item):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(item,ensure_ascii=False) + '\n')

def main(offset):
    # 获取url
    url = get_url(offset=offset*10)
    # 获取一个页面的html
    html = get_one_page(url)
    # 解析html提取出想要的items
    items = parse_one_page(html)
    # 存入文件
    for item in items:
        print(item)
        save_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(i)
