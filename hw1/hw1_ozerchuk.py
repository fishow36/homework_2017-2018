import urllib.request
import re

def get_page():
    req = urllib.request.Request('http://polkrug.ru/')
    with urllib.request.urlopen(req) as response:
       html = response.read().decode('utf-8')
    return(html)

def get_titles():
    html = get_page()
    reg_title = re.compile('<h3>.*?</h3>', flags= re.DOTALL)
    titles = reg_title.findall(html)
    return(titles)


def clear_titles():
    titles = get_titles()
    regTag = re.compile('<.*?>', re.DOTALL)
    regSpace = re.compile('\s{2,}', re.DOTALL)

    with open('news_titles.txt', 'w', encoding = 'utf-8') as text:
        for i in titles:
            i = regSpace.sub("", i)
            i = regTag.sub("", i)
            text.write(i + '\n')

def main():
    clear_titles()
        

if __name__ == '__main__':
    main()
