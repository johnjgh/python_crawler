import requests,time,os

def open_url(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
               'Referer':'http://pvp.qq.com/web201605/herolist.shtml',
               }
    html = requests.get(url,headers = headers)
    return html

def get_hero(html):
    hero_list = html.json()
    print(hero_list)
    for each in hero_list:
        folderdirs = r'E:\KPLskins\%s' % each['cname']
        if not os.path.exists(folderdirs):
            os.makedirs(folderdirs)
            os.chdir(folderdirs)
            hero_num = each['ename']
            skins_list = each['skin_name'].split('|')
            print('正在下载%s的皮肤' % each['cname'])
            download_photo(hero_num,skins_list)

def download_photo(hero_num, skins_list):
    for i in range(len(skins_list)):
        photo_url = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/%s/%s-bigskin-%d.jpg' % (hero_num,hero_num,i+1)
        photo_name = '%s.jpg' % skins_list[i]
        print(skins_list[i], photo_url)
        img = open_url(photo_url)
        with open(photo_name,'wb') as f:
            f.write(img.content)
    time.sleep(3)

if __name__ == '__main__':
    url = 'http://pvp.qq.com/web201605/js/herolist.json'
    print('开始下载英雄皮肤')
    get_hero(open_url(url))
    print('下载完成，just enjoy it')