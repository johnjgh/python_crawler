import requests,re,time,json,os

def open_url(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
               'Referer':'https://lol.qq.com/data/info-heros.shtml'
               }
    html = requests.get(url,headers = headers)
    return html

def get_heroid(html):
    a = r'"keys":(.*?),"data"'
    hero_str = re.findall(a,html)
    hero_dic = json.loads(hero_str[0])
    for key in hero_dic:
        print(hero_dic[key])
        get_heroname(hero_dic[key])

def get_heroname(id):
    hero_js = 'https://lol.qq.com/biz/hero/%s.js' % id
    b = r'"data":(.*?),"tags":'
    c = r'"skins":(.*?),"info"'
    html = open_url(hero_js).text
    data_dic = json.loads(re.findall(b,html)[0] + '}')
    skins_list = json.loads(re.findall(c,html)[0])
    print('开始下载%s的皮肤' % data_dic['title'])
    download_photo(data_dic,skins_list)

def download_photo(data_dic,skins_list):
    folderdir = r'E:\LOLskins\%s' % data_dic['title']
    if not os.path.exists(folderdir):
        os.makedirs(folderdir)
        os.chdir(folderdir)
        for each in skins_list:
            photo_url = 'http://ossweb-img.qq.com/images/lol/web201310/skin/big%s.jpg' % each['id']
            # 如果num是0，说明该皮肤是默认皮肤，其名称在data_dic中
            if not each['num']:
                photo_name = '%s.jpg' % data_dic['name']
            else:
                for i in each['name']:
                    if i in ['<','>','/','\\','|',':','\"','*','?']:
                        each['name'] = each['name'].replace(i,'_')
                photo_name = '%s.jpg' % each['name']
            html = open_url(photo_url)
            with open(photo_name,'wb') as f:
                print(photo_name.replace('.jpg',''), photo_url)
                f.write(html.content)
        time.sleep(3)

if __name__ == '__main__':
    url = 'http://lol.qq.com/biz/hero/champion.js'
    print('开始下载英雄皮肤')
    get_heroid(open_url(url).text)
    print('所有皮肤下载完成，enjoy it！！！')