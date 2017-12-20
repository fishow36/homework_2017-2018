import sqlite3
import matplotlib
import matplotlib.pyplot as plt

conn = sqlite3.connect('hittite.db')
c = conn.cursor()
connec = sqlite3.connect('glosses.db')
b = connec.cursor()
c.execute('Select * FROM wordforms')
rows = c.fetchall()
for i in rows:
    i = str(i)
    i = i[1:-1]
    i = i.split(',')
rows = list(rows)
b.execute('CREATE TABLE IF NOT EXISTS wordforms (id, Lemma, Wordform, Glosses)')
b.execute('CREATE TABLE IF NOT EXISTS glosses (id, Glosses, Meaning)')
b.execute('CREATE TABLE IF NOT EXISTS wordsglosses(idword, idgloss)')

for i in range(len(rows)):
    b.execute('INSERT INTO wordforms VALUES (?, ?, ?, ?)',(i+1, rows[i][0], rows[i][1], rows[i][2]))

with open ('glosses.txt', 'r', encoding ='utf-8') as f:
    text = f.readlines()
for i in range(len(text)):
    text[i] = text[i][:-1]
    text[i] = text[i].split(' — ')
    b.execute('INSERT INTO glosses VALUES (?, ?, ?)', (i+1, text[i][0], text[i][1]))
    
b.execute('SELECT id, Glosses FROM wordforms')
gl_rows = b.fetchall()
b.execute('SELECT id, Glosses from glosses')
gloss_list = b.fetchall()
for i in range(len(gl_rows)):
    gl_rows[i] = str(gl_rows[i])[1:-2]
    
    gl_rows[i] = gl_rows[i].split(',')
    gl_rows[i][1] = gl_rows[i][1][2:]
    gl_rows[i][1] = gl_rows[i][1].split('.')
gl_rows = list(gl_rows)

#print(gl_rows)
gloss_dict = {}
for i in gloss_list:
    i = str(i)
    i = i[1:-1]
    i = i.split(',')
    gloss_dict[i[1][2:-1]] = i[0]
#print(gloss_dict)

speechpart = {}

for i in range(len(gl_rows)):
    for j in gl_rows[i][1]:
        for key in gloss_dict:
            if key ==j:
                b.execute('INSERT INTO wordsglosses VALUES (?, ?)', (gl_rows[i][0], gloss_dict[key]))
                if key in speechpart:
                    speechpart[key]+=1
                else:
                    if j!= 'NEG':
                        speechpart[key] = 1
connec.commit()
xparts = []
ynumber = []
x = []
k = 0
for key in speechpart:
    xparts.append(key)
    ynumber.append(speechpart[key])
    k+=1
    x.append(k)
print(xparts)
print(ynumber)
print(x)
plt.xticks(x, xparts)
plt.bar(x, ynumber)
plt.show()
                
    

