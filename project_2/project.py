from flask import Flask
from flask import url_for, render_template, request, redirect
import os, re, json
app = Flask(__name__)

def create_table():
    if not os.path.exists('statistics.csv'):
        with open ('statistics.csv', 'a', encoding = 'utf-8') as table:
            table = table.write('native language' + ';' + 'age'+ ';' + 'answer1' + ';' + 'answer2' + ';' + 'answer3' + ';' + 'answer4' + ';' + 'answer5' +';'+ '\n')

def create_infolist():
    with open ('statistics.csv', 'r', encoding = 'utf-8') as table:
        table_list = table.readlines()
    info_list = []
    for i in range(1, len(table_list)):
        i_split = table_list[i].split(';')
        i_split.remove('\n')
        person_dict = {'nat_lang':i_split[0], 'age':i_split[1], 'answer1':i_split[2], 'answer2':i_split[3], 'answer3':i_split[4], 'answer4':i_split[5], 'answer5':i_split[6]}
        info_list.append(person_dict)
    return(info_list)

@app.route('/')
def index_main():
    return render_template('home.html')

@app.route('/thanks')
def index_thanks():        
    answers = []
    if request.args:
        lang = request.args['nat_lang']
        age = request.args['age']
        answer1 = request.args['answer1']
        answer2 = request.args['answer2']
        answer3 = request.args['answer3']
        answer4 = request.args['answer4']
        answer5 = request.args['answer5']
        with open ('statistics.csv', 'a', encoding = 'utf-8') as table:
            table = table.write(lang + ';' + age + ';' + answer1 + ';'+ answer2 + ';'+ answer3 + ';'+ answer4 + ';'+ answer5 + ';'+ '\n')
    return render_template('thanks.html')

@app.route('/stats')
def index_stats():
    infolist = create_infolist()
    lang = {}
    age = {}
    answer1 = {'1':0, '2':0, '3':0}
    answer2 = {'1':0, '2':0, '3':0}
    answer3 = {'1':0, '2':0, '3':0}
    answer4 = {'1':0, '2':0, '3':0}
    answer5 = {'1':0, '2':0, '3':0}
    for i in infolist:
        if i['nat_lang'] not in lang:
            lang[i['nat_lang']] = 1
        else:
            lang[i['nat_lang']] +=1
           
        if i['age'] not in age:
            age[i['age']] = 1
        else:
            age[i['age']] +=1
            

        answer1[i['answer1']] +=1 
        
        answer2[i['answer2']] +=1 
        
        answer3[i['answer3']] +=1 
        
        answer4[i['answer4']] +=1 
        
        answer5[i['answer5']] +=1 
    
    return render_template('stats.html', gr1 = answer1['3'], hgr1 = answer1['2'], ngr1 = answer1['1'],
                           gr2 = answer2['3'], hgr2 = answer2['2'], ngr2 = answer2['1'],
                           gr3 = answer3['3'], hgr3 = answer3['2'], ngr3 = answer3['1'],
                           gr4 = answer4['3'], hgr4 = answer4['2'], ngr4 = answer4['1'],
                           gr5 = answer5['3'], hgr5 = answer5['2'], ngr5 = answer5['1'],
                           lang = lang, age = age)

@app.route('/json')
def index_json():
    json_list = create_infolist()
    return render_template('json.html', json_raw = json.dumps(json_list,ensure_ascii = False))

@app.route('/search')
def index_search():
    return render_template('search.html')

@app.route('/results')
def index_results():
    searchlist = []
    searchoutput = []
    if request.args:
        nat_lang = request.args.get('nat_lang')
        agelow = request.args['agelow']
        agehigh = request.args['agehigh']
        infolist = create_infolist()
        for i in infolist:
            for age in range(int(agelow), int(agehigh)+1):
                if i['nat_lang'] == nat_lang and i['age'] == str(age):
                    searchlist.append(i)
        for i in range(len(searchlist)):
            for j in searchlist[i]:
                if j == 'nat_lang':
                    searchoutput.append('Родной язык' + ' - ' + str(searchlist[i][j]))
                if j == 'age':
                    searchoutput.append('Возраст' + ' - ' + str(searchlist[i][j]))
                if j == 'answer1':
                    searchoutput.append('Мӓ клубеш Васяде кенӓ.' + ' - ' + str(searchlist[i][j]))
                if j == 'answer2':
                    searchoutput.append('Тӓ корным марынде мода.' + ' - ' + str(searchlist[i][j]))
                if j == 'answer3':
                    searchoutput.append('Мӹнь шӹшердеок кашам шолтым.' + ' - ' + str(searchlist[i][j]))
                if j == 'answer4':
                    searchoutput.append('Йӹлмӹм пӓлӹмӓшде вес сӓндӓлӹкӹштӹ нӹлӹм пӓшӓм муаш.' + ' - ' + str(searchlist[i][j]))
                if j == 'answer5':
                    searchoutput.append('Йӹлмӹм пӓлӹмӹде вес сӓндӓлӹкӹштӹ нӹлӹм пӓшӓм муаш.' + ' - ' + str(searchlist[i][j]))
            searchoutput.append('\n')
        return render_template('results.html', natlang = nat_lang, result = searchoutput, agelow = agelow, agehigh = agehigh)
    return render_template('results.html')

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
