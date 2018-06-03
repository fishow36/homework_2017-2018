import gensim, logging, sys
import pymorphy2
from pymorphy2 import MorphAnalyzer
import networkx as nx
import matplotlib.pyplot as plt 
morph = MorphAnalyzer()

m = 'ruscorpora_upos_skipgram_300_5_2018.vec.gz'
if m.endswith('.vec.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
elif m.endswith('.bin.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
else:
    model = gensim.models.KeyedVectors.load(m)
model.init_sims(replace=True)
words = []
word = input('Введите слово для формирования семантического поля: ')
for i in morph.parse(word):
    if i.normal_form == word:
        part = str(i.tag).split(',')[0]
        if part == 'ADJF' or part == 'ADJS':
            word = word + '_ADJ'
        else:
            if part == 'INFN':
                word = word + '_VERB'
            
            else:
                word = word + '_' + part
        break
    else:
        print('Модель не знает такого слова или вы ввели его не в Именительном падеже :( ')

for i in model.most_similar(positive=[word], topn=20):
    print(i[0])
    words.append(i[0])


G = nx.Graph()
for i in range(len(words)):
    G.add_node(words[i])
for i in range(len(words)-1):
    for k in range (i+1, len(words)):
        if model.similarity(words[i], words[k]) > 0.5:
            G.add_edge(words[i], words[k])


pos=nx.spring_layout(G)

nx.draw_networkx_nodes(G, pos, node_color='red', node_size=50) # рисуем узлы красным цветом, задаём размер узла
nx.draw_networkx_edges(G, pos, edge_color='blue') # рисуем рёбра жёлтым
nx.draw_networkx_labels(G, pos, font_size=12, font_family='Arial')
plt.axis('off') # по умолчанию график будет снабжён осями с координатами, здесь они бессмысленны, так что отключаем
plt.show() # что получилось?

print('Коэффициент кластеризации: ' + str(nx.average_clustering(G)))
deg = nx.degree_centrality(G)
print('Пять самых центральных узлов графа: ')
for nodeid in range(1, 5):
    print(sorted(deg, key=deg.get, reverse=True)[nodeid])
graphs = list(nx.connected_component_subgraphs(G))
for i in range(len(graphs)):
    print('Радиус компоненты связности ' + str(i+1) + ': ' + str(nx.radius(graphs[i])))
