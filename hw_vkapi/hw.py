import urllib.request
import json
import sys
import re
import os
import os.path
import matplotlib.pyplot as plt
import datetime
from matplotlib import style
import matplotlib

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

##print(x.translate(non_bmp_map))

## выкачиваем первый пост. В нём смотрим, сколько постов на стене и узнаем, сколько реквестов надо сделать
def findnumberofrequests(url):
    response = urllib.request.urlopen(url) 

    result = response.read().decode('utf-8', errors='ignore')
    result_json = json.loads(result)
    number_of_posts = result_json['response']['count']
    number_of_requests = number_of_posts//100 + 1 ## один раз уже обратились, надо теперь ещё
    ##print(result_json) ## чтобы видеть как это устроено
    return number_of_requests

def download100posts(link):
    req = urllib.request.Request(link)
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8', errors='ignore')
    return (result)

def makejsonlist_posts(number_of_requests):
    result_all = []
    for i in range (0, number_of_requests): ## это будет после того как скачалось первый раз
        reg_request = 'https://api.vk.com/method/wall.get?owner_id=-161180646&count=100&v=5.73&access_token=45f3abe245f3abe245f3abe288459187d2445f345f3abe21f3262af14cc7739a310fd56&offset=' + str(i*100)
        for j in json.loads(download100posts(reg_request))['response']['items']:
            result_all.append(j)
    return(result_all)

def makejsonlist_comments(number_of_requests, post_id): ## комменты к одному посту
    result_all = []
    for i in range (0, number_of_requests):
        reg_request = 'https://api.vk.com/method/wall.getComments?owner_id=-161180646&count=100&filter_owner&v=5.73&access_token=45f3abe245f3abe245f3abe288459187d2445f345f3abe21f3262af14cc7739a310fd56&offset=' + str(i*100) + '&post_id=' + str(post_id)
        for j in json.loads(download100posts(reg_request))['response']['items']:
            result_all.append(j)
    return (result_all)

    


def writeposts(listofposts):
    full_json = {}
    if not os.path.exists('posts'):
        os.mkdir('posts')
    for i in listofposts:
        listofcomments = makejsonlist_comments((i['comments']['count'])//100 + 1, i['id'])
        dictvalue = []
        dictvalue.append(i)
        dictvalue.append(listofcomments)
        full_json[i['id']] = dictvalue
            
##            with open (os.path.join('posts', (str(j['id']) +  '.txt') ), 'a', encoding = 'utf-8') as f:
##                f.write(j['text'].translate(non_bmp_map))
##                for k in listofcomments:
##                    for m in k['response']['items']:
##                        f.write(m['text'].translate(non_bmp_map))
    if not os.path.exists('fulljson.json'):
        with open ('fulljson.json', 'w', encoding = 'utf-8') as d:
            d.write(json.dumps(full_json, ensure_ascii=False))
    return full_json

def openjson():
    with open ('fulljson.json', 'r', encoding = 'utf-8') as f:
        fulljson = json.loads(f.read())
    return fulljson

def length_words(text):
    text = re.sub('\n', ' ', text)
    text = text.split(' ')
    length = len(text)
    return length

    
def totallength_amount(listofcomments): ##возвращает массив с общей длиной всех комментов и их кол-вом
    list_totallength_amount = []
    total_length = 0
    for i in listofcomments:        
        total_length += length_words(i['text'])
    list_totallength_amount.append(total_length)
    list_totallength_amount.append(len(listofcomments))
    return(list_totallength_amount)

def averagelencomm(fulljson):
    dict_len = {}
    x_lenpost = []
    y_lencomm = []
    for i in fulljson:
        post_length = length_words(fulljson[i][0]['text'])
        comm_lenandamount = totallength_amount(fulljson[i][1])
        if post_length in dict_len:
            dict_len[post_length][0] += comm_lenandamount[0]
            dict_len[post_length][1] += comm_lenandamount[1]
        else:
            dict_len[post_length] = comm_lenandamount
    for key in sorted(dict_len.keys()):
        x_lenpost.append(key)
        y_lencomm.append(dict_len[key][0]/dict_len[key][1])
    plt.bar(x_lenpost, y_lencomm)
    plt.title('Отношение длины поста к средней длине его комментариев')
    plt.xlabel('Длина поста')
    plt.ylabel('Средняя длина комментариев')
    plt.show()

def countage(bdate):
    now = datetime.datetime.now()
    birthdate = bdate.split('.')
    if now.month >= int(birthdate[1]):
        if now.day >= int(birthdate[0]):
            age = now.year - int(birthdate[2])
        else:
            age = now.year - int(birthdate[2])-1
    else:
        age = now.year - int(birthdate[2])-1
    return age

def findallcity(allids):
    result_dict = {}
    for ids in allids:            
        req = 'https://api.vk.com/method/users.get?v=5.73&fields=city&user_ids=' + str(ids)
        response = urllib.request.urlopen(req) 
        result = response.read().decode('utf-8', errors='ignore')
        result_json = json.loads(result)['response']
        for i in result_json:
            if 'city' in i:
                result_dict[str(i['id'])] = i['city']['title']
    return result_dict

def findallage(allids):
    result_dict = {}
    for ids in allids:            
        req = 'https://api.vk.com/method/users.get?v=5.73&fields=bdate&user_ids=' + str(ids)
        response = urllib.request.urlopen(req) 
        result = response.read().decode('utf-8', errors='ignore')
        result_json = json.loads(result)['response']
        for i in result_json:
            if 'bdate' in i and len(i['bdate'].split('.')) == 3:
                result_dict[str(i['id'])] = countage(i['bdate'])
    return result_dict

def findallids(fulljson):
    allids = []
    for i in fulljson:
        if 'signer_id' in fulljson[i][0]:
            if fulljson[i][0]['signer_id'] > 0 and fulljson[i][0]['signer_id'] not in allids:
                allids.append(fulljson[i][0]['signer_id'])
        for j in fulljson[i][1]:
            if j['from_id'] > 0 and j['from_id'] not in allids:
                allids.append(j['from_id'])
    return(allids)
            
        
    
def averagelencity(fulljson, dictcity, rotation, names):
    dict_citypost = {}
    dict_citycomm = {}
    x_citypost = []
    y_lenpost= []
    x_citycomm = []
    y_lencomm = []
    for i in fulljson: ##этот цикл для постов
        if 'signer_id' in fulljson[i][0]:
            if str(fulljson[i][0]['signer_id']) in dictcity: ##fulljson[i][0]['signer_id'] > 0 and 
                post_length = length_words(fulljson[i][0]['text'])
                city = dictcity[str(fulljson[i][0]['signer_id'])]
                if city in dict_citypost:
                    dict_citypost[city][0] += post_length
                    dict_citypost[city][1] +=1
                else:
                    dict_value = []
                    dict_value.append(post_length)
                    dict_value.append(1)
                    dict_citypost[city] = dict_value
    for key in sorted(dict_citypost.keys()):
        x_citypost.append(str(key))
        y_lenpost.append(dict_citypost[key][0]/dict_citypost[key][1])
        
    for i in fulljson: ##этот цикл для комментов
        for j in fulljson[i][1]:
            if  str(j['from_id']) in dictcity:
                post_length = length_words(j['text'])
                city = dictcity[str(j['from_id'])]
                if city in dict_citycomm:
                    dict_citycomm[city][0] += post_length
                    dict_citycomm[city][1] +=1
                else:
                    dict_value = []
                    dict_value.append(post_length)
                    dict_value.append(1)
                    dict_citycomm[city] = dict_value
    for key in sorted(dict_citycomm.keys()):
        if dict_citycomm[key][1] >=10:
            x_citycomm.append(str(key))
            y_lencomm.append(dict_citycomm[key][0]/dict_citycomm[key][1])

    font = {'size'   : 7}
    matplotlib.rc('font', **font)
    names_list = names.split(';')

    plt.bar(x_citypost, y_lenpost)
    plt.title(names_list[0])
    plt.xlabel(names_list[1])
    plt.ylabel(names_list[2])
    if rotation == 1:
        plt.xticks(range(len(x_citypost)), x_citypost, rotation = 90)
    plt.show()
    plt.bar(x_citycomm, y_lencomm)
    plt.title(names_list[3])
    plt.xlabel(names_list[4])
    plt.ylabel(names_list[5])
    if rotation == 1:
        plt.xticks(range(len(x_citycomm)), x_citycomm, rotation = 90)
    plt.show()

def main():
    req_posts = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=-161180646&count=1&offset=1&v=5.73&access_token=45f3abe245f3abe245f3abe288459187d2445f345f3abe21f3262af14cc7739a310fd56')
    numberofrequests = findnumberofrequests(req_posts)

    if os.path.exists('fulljson.json'):
        with open('fulljson.json', 'r', encoding = 'utf-8') as f:
            allposts = json.loads(f.read())
    else:
        posts = makejsonlist_posts(numberofrequests)
        allposts = writeposts(posts)

    if os.path.exists('allids.json'):
        with open ('allids.json', 'r', encoding  = 'utf-8') as f:
            allids = json.loads(f.read())
    else:
        allids  = findallids(allposts)    
        with open ('allids.json', 'w', encoding = 'utf-8') as f:
            f.write(json.dumps(allids))

    if os.path.exists('allcities.json'):
        with open ('allcities.json', 'r', encoding = 'utf-8') as d:
            citydict = json.loads(d.read())
    else:
        citydict = findallcity(allids)
        with open ('allcities.json', 'w', encoding = 'utf-8') as f:
            f.write(json.dumps(citydict, ensure_ascii=False))

    if os.path.exists('allages.json'):
        with open ('allages.json', 'r', encoding = 'utf-8') as f:
            agedict = json.loads(f.read())
    else:
        agedict = findallage(allids)
        with open ('allages.json', 'w', encoding = 'utf-8') as f:
            f.write(json.dumps(agedict, ensure_ascii=False))
    averagelencity(allposts, citydict, 1, 'Средние длины постов для каждого города;Название города;Средняя длина поста;Средние длины комментариев для каждого города;Название города;Средняя длина комментария')
    averagelencity(allposts, agedict, 0, 'Средние длины постов для каждого возраста;Возраст;Средняя длина поста;Средние длины комментариев для каждого возраста;Возраст;Средняя длина комментария')

    averagelencomm(allposts)
if __name__ == '__main__':
    main()


