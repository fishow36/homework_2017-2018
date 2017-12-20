from flask import Flask
from flask import request
from flask import render_template
import urllib.request
import html
import re
import json
import os

app = Flask(__name__)

def russian_dictionary():    
    rusdict = {}
    urls_list = ['http://www.dorev.ru/ru-index.html?l=c0',
             'http://www.dorev.ru/ru-index.html?l=c1',
             'http://www.dorev.ru/ru-index.html?l=c2',
             'http://www.dorev.ru/ru-index.html?l=c3',
             'http://www.dorev.ru/ru-index.html?l=c4',
             'http://www.dorev.ru/ru-index.html?l=c5',
             'http://www.dorev.ru/ru-index.html?l=c6',
             'http://www.dorev.ru/ru-index.html?l=c7',
             'http://www.dorev.ru/ru-index.html?l=c8',
             'http://www.dorev.ru/ru-index.html?l=c9',
             'http://www.dorev.ru/ru-index.html?l=ca',
             'http://www.dorev.ru/ru-index.html?l=cb',
             'http://www.dorev.ru/ru-index.html?l=cc',
             'http://www.dorev.ru/ru-index.html?l=cd',
             'http://www.dorev.ru/ru-index.html?l=ce',
             'http://www.dorev.ru/ru-index.html?l=cf',
             'http://www.dorev.ru/ru-index.html?l=d0',
             'http://www.dorev.ru/ru-index.html?l=d1',
             'http://www.dorev.ru/ru-index.html?l=d2',
             'http://www.dorev.ru/ru-index.html?l=d3',
             'http://www.dorev.ru/ru-index.html?l=d5',
             'http://www.dorev.ru/ru-index.html?l=d6',
             'http://www.dorev.ru/ru-index.html?l=d7',
             'http://www.dorev.ru/ru-index.html?l=d8',
             'http://www.dorev.ru/ru-index.html?l=d9',
             'http://www.dorev.ru/ru-index.html?l=da',
             'http://www.dorev.ru/ru-index.html?l=db',
             'http://www.dorev.ru/ru-index.html?l=dc',
             'http://www.dorev.ru/ru-index.html?l=dd',
             'http://www.dorev.ru/ru-index.html?l=de',
             'http://www.dorev.ru/ru-index.html?l=df']

             
             
    for i in urls_list:
        with urllib.request.urlopen(i) as response:
            htmll = response.read().decode('windows-1251')
            regwords = re.compile('<td class="uu">([А-Яа-я]*?)</td><td></td><td class="uu">(.*?)</td>', re.DOTALL)
            words = re.findall(regwords, htmll)
            for i in words:
                rusdict[i[0]] = i[1]
    for i in rusdict:
        if re.search(r'&nbsp;', rusdict[i]):
            rusdict[i] = re.sub(r'&nbsp;', '', rusdict[i])
        if re.search(r'<.*?>', rusdict[i]):
            rusdict[i] = re.sub(r'<.*?>', '', rusdict[i])
        rusdict[i] = html.unescape(rusdict[i])
        if re.search (',', rusdict[i]):
           rusdict[i] = re.sub(',.*', '', rusdict[i])
        if re.search (' ', rusdict[i]):
            rusdict[i] = re.sub(' .*', '', rusdict[i])
        if re.search ('\'', rusdict[i]):
            rusdict[i] = re.sub('\'', '', rusdict[i])
        i = lower(i)
        rusdict[i] = lower(rusdict[i])
    with open ('rusdict.txt', 'w', encoding = 'utf-8') as f:
        json.dump(rusdict, f, ensure_ascii = False)
    return rusdict


def weather():
    with urllib.request.urlopen('https://yandex.ru/pogoda/skopje') as response:
        htmll = response.read().decode('utf-8')

    condition = re.search('<div class="fact__condition(.*?)>(.*?)</div>', htmll).group(2)
    temperature = re.search('<div class="temp fact__temp"><span class="temp__value">(.*?)</span>', htmll).group(1)
    return(condition + ', ' + temperature + '°')

def find_ending(wordnom, wordobl): ##окончание косвенного и номер с которого окончания ном
    for i in range(len(wordnom)):
        
        if wordnom[:i+1] in wordobl:
            ending_obl = ''
            base = wordnom[:i+1]
            ending_obl = wordobl[i+1:]
            ending_nom_number = str(i+1)
            output = ending_obl + ',' + ending_nom_number
    if len(ending_obl) == 0:
        output = ',' + str(len(wordnom))
    return output

def find_wordobl(mystem_entry):
    re_wordobl = re.compile('([А-Я]?[а-я]+){')
    wordobl = re.search(re_wordobl, mystem_entry).group(1)
    wordobl = wordobl.lower()
    return (wordobl)

def find_wordnom(mystem_entry):
    re_wordnom = re.compile('{([а-я]+)=')
    if re.search(re_wordnom, mystem_entry):        
        wordnom = re.search(re_wordnom, mystem_entry).group(1)
    else:
        wordnom = find_wordobl(mystem_entry)
    return (wordnom)

def is_number_plorsg(mystem_entry):
    if re.search('мн', mystem_entry):
        number = 'pl'
    else:
        number = 'sg'
    return(number)

def is_case_datorabl(mystem_entry):
    re_case = re.compile('од=([а-я]+)[\|},]')
    if re.search (re_case, mystem_entry):
        case = re.search(re_case, mystem_entry).group(1)
        if case == 'дат' or case == 'пр':
            case_val = True
        else:
            case_val = False
    else:
        case_val = False
    return (case_val)

def is_case_nomoracc(mystem_entry):
    re_case = re.compile('од=([а-я]+)[\|},]')
    if re.search(re_case, mystem_entry):
        case = re.search(re_case, mystem_entry).group(1)
        if case == 'им' or case == 'вин':
            case_val = True
        else:
            case_val = False
    else:
        case_val = False
    return (case_val)
def find_gender(mystem_entry):
    if re.search('жен', mystem_entry):
        gender = 'f'
    elif re.search('муж', mystem_entry):
        gender = 'm'
    else:
        gender = 'n'
    return(gender)

def prerev(wordnom, rusdict):
    for key in rusdict:
        if wordnom == key:
            wordnom = rusdict[key]
    return (wordnom)


@app.route('/')
def russian_word():
    ##russian_dictionary() - сайт перестал выдавать хтмл, поэтому не выкачиваю словарь, а использую выкачанный ранее
    rusdict = json.load(open('rusdict.json', encoding = 'utf-8'))
    if request.args:      
        f = request.args['russian_word']
        if f in rusdict:
            newort = rusdict[f]
        else:
            newort = f
        return render_template('hzht.html', name = newort,weather_skopje = weather())
    return render_template('hzht.html', weather_skopje = weather())

@app.route('/news')
def news_dorev():
    rusdict = json.load(open('rusdict.json', encoding = 'utf-8'))

##    with urllib.request.urlopen('https://www.kommersant.ru/') as response:
##        html_kom = response.read().decode('windows-1251')
##    cyryl = re.findall('([А-Я]*[а-я]*)?', html_kom)
##    with open('html_kom.txt', 'w', encoding = 'utf-8') as f:
##        for i in cyryl:
##            if i != '':
##                f.write(i + ' ')
##
##    os.system('mystem.exe '+ '-di '+ ' html_kom.txt ' + 'kom_mystem.txt')

    with open ('kom_mystem.txt', 'r', encoding = 'utf-8') as f:
        text = f.read()

    regex = re.compile('([А-Я]?[а-я]+{.*?((\|)|(})))')
    massiv = re.findall(regex, text)
    newmas = []
    for i in massiv:
        newmas.append(i[0])

    reg_speechpart = re.compile('[А-Я]?[а-я]+{.*?=(.*?)(,|=)')
    listtoprint = []

    consonants = ['б', 'в','г','д','ж','з','к','л','м','н','п','р','с','т','ф','х','ц','ч','ш','щ']
    vowels = ['ё','у','е','ы','а','о','э','я','и','ю']
    nom_dict = {}
    for val, stroka in enumerate(newmas): ##done
        if re.search(reg_speechpart, stroka):
            if re.search(reg_speechpart, stroka).group(1) == 'A' or re.search(reg_speechpart, stroka).group(1) == 'ANUM' or re.search(reg_speechpart, stroka).group(1) == 'APRO':
                wordnom = find_wordnom(stroka)
                if wordnom in nom_dict:
                    nom_dict[wordnom] +=1
                else:
                    nom_dict[wordnom] = 1
                wordobl = find_wordobl(stroka)
                number = is_number_plorsg(stroka)
                if val != len(newmas)-1:
                    gender = find_gender(newmas[val+1])
                    case = is_case_nomoracc(newmas[val+1])
                else:
                    gender = find_gender(newmas[val])
                    case = is_case_nomoracc(newmas[val])
                if wordnom[0] == wordobl[0]:
                    output = find_ending(wordnom, wordobl)
                    ending_obl = output.split(',')[0]
                    numberending_nom = int(output.split(',')[1])
                wordnom = prerev(wordnom, rusdict)
                if wordnom[0] == wordobl[0]:
                    wordnom = wordnom[:numberending_nom] + ending_obl
                if gender != 'm' and case and re.search('(і|и|ы)е(ся)?$', wordnom):
                    i = wordnom.rfind('е')
                    wordnom = wordnom[:i] + 'я' + wordnom[i+1:]
                listtoprint.append(wordnom)

            elif re.search(reg_speechpart, stroka).group(1) == 'S' or re.search(reg_speechpart, stroka).group(1) =='SPRO' or re.search(reg_speechpart, stroka).group(1) == 'NUM': ## done
                wordnom = find_wordnom(stroka)
                if wordnom in nom_dict:
                    nom_dict[wordnom] +=1
                else:
                    nom_dict[wordnom] = 1
                wordobl = find_wordobl(stroka)
                number = is_number_plorsg(stroka)
                casedatorabl = is_case_datorabl(stroka)
                if wordnom[0] == wordobl[0]:
                    output = find_ending(wordnom, wordobl)
                    ending_obl = output.split(',')[0]
                    numberending_nom = int(output.split(',')[1])
                
                wordnom = prerev(wordnom, rusdict)
                if wordnom[0] == wordobl[0]:
                    wordnom = wordnom[:numberending_nom] + ending_obl
                else: wordnom = wordobl
                if casedatorabl and number == 'sg':
                    if 'е' in wordnom[-len(ending_obl)+1:]:
                        i = wordnom.rfind('е')
                        wordnom = wordnom[:i] + 'ѣ' + wordnom[i+1:]
                listtoprint.append(wordnom)

            elif re.search(reg_speechpart, stroka).group(1) == 'V': ##done
                wordnom = find_wordnom(stroka)
                if wordnom in nom_dict:
                    nom_dict[wordnom] +=1
                else:
                    nom_dict[wordnom] = 1
                wordobl = find_wordobl(stroka)
                output = find_ending(wordnom, wordobl)
                ending_obl = output.split(',')[0]
                numberending_nom = int(output.split(',')[1])
                wordnom = prerev(wordnom, rusdict)
                wordnom = wordnom[:numberending_nom] + ending_obl
                wordnom = listtoprint.append(wordnom)
            elif re.search(reg_speechpart, stroka).group(1) == 'PR' or re.search(reg_speechpart, stroka).group(1) == 'ADV' or re.search(reg_speechpart, stroka).group(1) == 'ADVPRO' or re.search(reg_speechpart, stroka).group(1) == 'PART' or re.search(reg_speechpart, stroka).group(1) == 'INTJ' or re.search(reg_speechpart, stroka).group(1) == 'CONJ' or re.search(reg_speechpart, stroka).group(1) == 'COM':
                wordnom = find_wordnom(stroka)
                if wordnom in nom_dict:
                    nom_dict[wordnom] +=1
                else:
                    nom_dict[wordnom] = 1
                wordnom = prerev(wordnom, rusdict)
                listtoprint.append(wordnom)
            else:
                wordnom = find_wordobl(stroka)                    
                if wordnom in nom_dict:
                    nom_dict[wordnom] +=1
                else:
                    nom_dict[wordnom] = 1
    maxval = 0
    maxwords = ['','','','','','','','','','',]
    for i in range(0, 10):
        maxval = 0
        for key in nom_dict:
            if nom_dict[key] > maxval:
                maxval = nom_dict[key]
                print(maxval)
                maxwords[i] = key
        nom_dict.pop(maxwords[i])
                
            
    for i, word in enumerate(listtoprint):
        for j in consonants:
            if listtoprint[i][len(listtoprint[i])-1] == j:
                listtoprint[i] = listtoprint[i] + 'ъ'
        if re.search('^бес', word):
            listtoprint[i] = re.sub('^бес', 'без', listtoprint[i])
        re_ivowel = re.compile('(и)(ё|у|е|ы|а|о|э|я|и|ю)')
        if re.search(re_ivowel, word):
            listtoprint[i] = re.sub(re.search(re_ivowel, listtoprint[i]).group(1), 'і', listtoprint[i], count = 1)

    return render_template('news_dorev.html', listtoprint = listtoprint, dicto = maxwords)


@app.route('/test')
def test_func():
    return render_template('test_yat.html')

@app.route('/results')
def results_func():
    if request.args:
        answers = []
        correct_answers = ['yat', 'yat', 'e', 'yat', 'yat', 'yat', 'e', 'e', 'yat', 'e', 'yat']
        numberofcorrect = []
        answers.append( request.args['answer1'])
        answers.append(request.args['answer2'])
        answers.append(request.args['answer3'])
        answers.append(request.args['answer4'])
        answers.append(request.args['answer5'])
        answers.append(request.args['answer6'])
        answers.append(request.args['answer7'])
        answers.append(request.args['answer8'])
        answers.append(request.args['answer9'])
        answers.append(request.args['answer10'])
        answers.append(request.args['answer11'])
        correct = 0
        for i in range(len(answers)):
            if answers[i] == correct_answers[i]:
                numberofcorrect.append(str(i+1) + ': Верно')
                correct+=1
            else:
                numberofcorrect.append(str(i+1) + ': Неверно')
           
        return render_template('results.html', answers = numberofcorrect, correct = correct)
    
if __name__ == '__main__':
    app.run(debug=True)
