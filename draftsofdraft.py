import urllib.request
import re

##req = urllib.request.Request('http://polkrug.ru/news/archive')## потом надо поменять на цикл который дает адреса следующих страниц в архиве



def get_urls(req): ##даёт ссылки на все статьи на одной странице
    re_header = re.compile(r'<h3>.*?<a href="(.*?)">.*?</a>.*?</h3>', flags = re.DOTALL)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    urls = re.findall(re_header, html)
    for i in range(len(urls)):
        urls[i] = 'http://polkrug.ru' + urls[i]
    return(urls)

def get_pagenumbers(): ##дает все ссылки на страницы архива
    pages_urls = []
    for i in range (1,3):
        pagenumber = 'http://polkrug.ru/news/archive?page=' + str(i)
        pages_urls.append(pagenumber)
    return(pages_urls)

def get_allurls(): ##дает все ссылки на нужные статьи
    all_urls = []
    pages_urls = get_pagenumbers()
    for i in pages_urls:
        all_urls = all_urls + get_urls(i)
    return(all_urls)


def whatsthat():
    all_urls = get_allurls()
    for i in all_urls:
        with urllib.request.urlopen(i) as response:
            html = response.read().decode('utf-8')
        reg_author = r'class="author_fio">(.*?)<'
        reg_header =r'<h1>(.*?)</h1>'
        reg_created = ##надо будет менять названия месяцев на номера........
        reg_topic = r'<a class="rubric" href=".*?">(.*?)</a>'
        reg_publ_year = ## вытащить из даты
##        with open ('metadata.csv', 'w', encoding = 'utf-8') as table:
whatsthat()            
        

    
##    for i in re.findall(re_header, html):## массив в котором лежат ссылки на статьи на этой странице архива
##        print('\n' + i)
##        req = urllib.request.Request('http://polkrug.ru' + i)
##        with urllib.request.urlopen(req) as response:
##            html= response.read().decode('utf-8')
##        
##
##надо
##найти номера страниц
##на каждой странице найти ссылки на статьи
##??? profit
