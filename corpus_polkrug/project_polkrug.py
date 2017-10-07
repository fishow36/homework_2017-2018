import urllib.request
import re
import os
import shutil
import time


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
    for i in range (1,72):
        pagenumber = 'http://polkrug.ru/news/archive?page=' + str(i)
        pages_urls.append(pagenumber)
    return(pages_urls)

def get_all_urls(): ##дает все ссылки на нужные статьи
    all_urls = []
    pages_urls = get_pagenumbers()
    for i in pages_urls:
        all_urls = all_urls + get_urls(i)
    return(all_urls)

def create_csv(): ##создает таблицу, в которой будут метаданные + создает папку невспапер
    if not os.path.exists('polkrug_newspaper'):
        os.mkdir('polkrug_newspaper')
    if not os.path.exists(os.path.join('newspaper', 'metadata.csv')):
        with open (os.path.join('polkrug_newspaper','metadata.csv'), 'a', encoding = 'utf-8') as table:
            table = table.write('path'+ ';' + 'author'+ ';' + 'sex'+ ';' + 'birthday'+ ';' + 'header'+ ';' + 'created'+ ';' + 'sphere'+ ';' + 'genre_fi'+ ';' + 'type'+ ';' + 'topic'+ ';' + 'chronotop'+ ';' + 'style'+ ';' + 'audience_age'+ ';' + 'audience_level'+ ';' + 'audience_size'+ ';' + 'source'+ ';' + 'publication'+ ';' + 'publisher'+ ';' + 'publ_year'+ ';' + 'medium'+ ';' + 'country'+ ';' + 'region'+ ';' + 'language')
        

def months_to_numbers(date):
    re_date = '(\d*?) (.*?) (\d*)'
    day = re.search(re_date, date).group(1)
    month = re.search(re_date, date).group(2)
    year = re.search(re_date, date).group(3)
    if month == 'января':
        month = '01'
    elif month == 'февраля':
        month = '02'
    elif month == 'марта':
        month = '03'
    elif month == 'апреля':
        month = '04'
    elif month == 'мая':
        month = '05'
    elif month == 'июня':
        month = '06'
    elif month == 'июля':
        month = '07'
    elif month == 'августа':
        month = '08'
    elif month == 'сентября':
        month = '09'
    elif month == 'октября':
        month = '10'
    elif month == 'ноября':
        month = '11'
    else:
        month = '12'
    date = day + '.' + month + '.' + year
    return(date)


def get_html(source):
    with urllib.request.urlopen(source) as response:
        html = response.read().decode('utf-8')
        html = source + '\n' + html
    return(html)
def get_metadata(html):## достаёт метаданные и записывает их в таблицу, возвращает чистый текст

    if re.search('class="author_fio">(.*?)<', html):
        author = ', '.join(re.findall('class="author_fio">(.*?)<', html))
    else:
        author = 'Noname'
    source = re.search(r'(http://polkrug.ru/news/.*?)\n', html).group(1)
    header =re.search('<h1>(.*?)</h1>', html).group(1)
    filename = re.search(r'/\d*?-(.*)', source).group(1)
    date = get_date(html)
    topic = re.search('<a class="rubric" href=".*?">(.*?)</a>', html).group(1)
    publ_year = date.split('.')[2]
    publ_month = date.split('.')[1]
    path = os.path.join('polkrug_newspaper', 'plain', publ_year, publ_month, filename) + '.txt'
    

    row = '%s;%s;;;%s;%s;публицистика;;;%s;;нейтральный;н-возраст;н-уровень;городская;%s;Полярный круг;;%s;газета;Россия;Ямало-Ненецкий автономный округ;ru'
    with open (os.path.join('polkrug_newspaper', 'metadata.csv'), 'a', encoding = 'utf-8') as table:
        table = table.write('\n' + row%(path, author, header, date, topic, source, publ_year))
    info = ['@au ' + author, '@ti ' + header, '@da ' + date, '@topic ' + topic, '@url ' + source]
    return(info)

def get_date(html):
    date = re.search('div class="news_date">(.*?)<', html).group(1)
    date = months_to_numbers(date)
    return(date)
def get_filename(html):
    source = re.search(r'(http://polkrug.ru/news/.*?)\n', html).group(1)
    filename = re.search(r'/\d*?-(.*)', source).group(1)
    return(filename)
def clean_text(html):##получает html, выдает норм текст
    text = re.findall('<p>(.*?)</p>', html)
    text.pop()
    
    text = '\n'.join(text)
    text = re.sub('<.*?>', '', text)
    text = re.sub('&nbsp;', '', text)
    text = re.sub('&ndash;', '–', text)
    text = re.sub('&laquo;', '«', text)
    text = re.sub('&raquo;', '»', text)
    return(text)

def sort_into_folders(info, filename, date, text):
    publ_year = date.split('.')[2]
    publ_month = date.split('.')[1]
    directories = [(os.path.join('polkrug_newspaper', 'plain')), (os.path.join('polkrug_newspaper', 'mystem-xml')), (os.path.join('polkrug_newspaper', 'mystem-plain'))]
    for i in directories:
        if not os.path.exists(os.path.join(i, publ_year, publ_month)):
            os.makedirs(os.path.join(i, publ_year, publ_month))
    with open(os.path.join('polkrug_newspaper', 'plain', publ_year, publ_month, filename) + '.txt', 'w', encoding = 'utf-8') as f:##plain text
        f = f.write(text)
    text_info = ''
    for i in info:
        text_info = text_info + i + '\n'
    text = text_info + text
    input_txt = 'polkrug_newspaper' + os.sep + 'plain' + os.sep + publ_year + os.sep + publ_month + os.sep + filename + '.txt '
    output_txt ='polkrug_newspaper' + os.sep + 'mystem-plain' + os.sep + publ_year + os.sep + publ_month + os.sep + filename + '.txt'
    output_xml = 'polkrug_newspaper' + os.sep + 'mystem-xml' + os.sep + publ_year + os.sep + publ_month + os.sep + filename + '.xml'
    os.system('mystem.exe '+ '-di '+ input_txt + output_txt) ##mystem-plain
    os.system('mystem.exe '+ '-di '+ input_txt + output_xml) ##mystem-xml
    
    with open(os.path.join('polkrug_newspaper', 'plain', publ_year, publ_month, filename) + '.txt', 'w', encoding = 'utf-8') as f:##plain text
        f = f.write(text)
        
def main():
    all_urls = get_all_urls()
    create_csv()
    for i in all_urls:
        html = get_html(i)
        info = get_metadata(html)
        text = clean_text(html)
        date = get_date(html)
        filename = get_filename(html)
        sort_into_folders(info, filename, date, text)
        time.sleep(5)
        
main()


