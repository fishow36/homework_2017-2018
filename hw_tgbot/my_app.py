from pymorphy2 import MorphAnalyzer
import re, random
import telebot
import conf
import flask

morph = MorphAnalyzer()



WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)
bot = telebot.TeleBot(conf.TOKEN, threaded=False)

bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)
def makewordlist():
    with open ('1grams-3.txt', 'r', encoding = 'utf-8') as f:
        grams = f.read()
    grams = grams.split('\n')
    noun = []
    adjf = []
    adjs = []
    comp = []
    verb = []
    infn = []
    prtf = []
    prts = []
    grnd = []
    numr = []
    advb = []
    npro = []
    pred = []
    prep = []
    conj = []
    prcl = []
    intj = []
    wordlist = []
    for i in grams:
        k = i.split('\t')[1]
        tag = morph.parse(k)[0].tag
        normal = morph.parse(k)[0].normal_form
        if 'NOUN' in tag and normal not in noun:
            noun.append(normal)
        else:
            if 'ADJF' in tag and normal not in adjf:
                adjf.append(normal)
            else:
                if 'ADJS' in tag and normal not in adjs:
                    adjs.append(normal)
                else:
                    if 'COMP' in tag and normal not in comp:
                        comp.append(normal)
                    else:
                        if 'VERB' in tag or 'INFN' and normal not in verb:
                            verb.append(normal)
                        else:
                            if 'PRTF' in tag and normal not in prtf:
                                prtf.append(normal)
                            else:
                                if 'PRTS' in tag and normal not in prts:
                                    prts.append(normal)
                                else:
                                    if 'GRND' in tag and normal not in grnd:
                                        grnd.append(normal)
                                    else:
                                        if 'NUMR' in tag and normal not in numr:
                                            numr.append(normal)
                                        else:
                                            if 'ADVB' in tag and normal not in advb:
                                                advb.append(normal)
                                            else:
                                                if 'NPRO' in tag and normal not in npro:
                                                    npro.append(normal)
                                                else:
                                                    if 'PRED' in tag and normal not in pred:
                                                        pred.append(normal)
                                                    else:
                                                        if 'PREP' in tag and normal not in prep:
                                                            prep.append(normal)
                                                        else:
                                                            if 'CONJ' in tag and normal not in conj:
                                                                conj.append(normal)
                                                            else:
                                                                if 'PRCL' in tag and normal not in prcl:
                                                                    prcl.append(normal)
                                                                else:
                                                                    if 'INTJ' in tag and normal not in intj:
                                                                        intj.append(normal)
                            
                    
    print(noun)             
    return noun, adjf, adjs, comp, verb, prtf, prts, grnd, numr, advb, npro, pred, prep, conj, prcl, intj

def inflection(listpart, tagset, oldinfl):
    newlemma = listpart[random.randint(0, len(listpart)-1)]
    newana = morph.parse(newlemma)[0]
    for i in tagset:
        for k in i.split(' '):
            try:
                inflected = newana.inflect({k})
            except TypeError:
                inflected = oldinfl
    return inflected

def changewords(text):
    noun, adjf, adjs, comp, verb, infn, prtf, prts, grnd, numr, advb, npro, pred, prep, conj, prcl, intj = makewordlist()
    text = input('Enter text: ')
    text = text.split(' ')
    commas = re.compile(',|\.|"|“|”|>|<|«|»|@|&|#|\+|=|[|]|{|}|\\\|\/|\*|:|;|—|(|)|\'|\|')
    for i in range(len(text)):
        text[i] = re.sub(commas, '', text[i])
        ana = morph.parse(text[i])[0]
        tag = ana.tag
        tagset = str(ana.tag).split(',')
        if 'NOUN' in tag:
            text[i] = inflection(noun, tagset, ana).word            
        else:
            if 'ADJF' in tag:
                text[i] = inflection(adjf, tagset, ana)
            else:
                if 'ADJS' in tag:
                    text[i] = inflection(adjs, tagset, ana)
                else:
                    if 'COMP' in tag:
                        text[i] = inflection(comp, tagset, ana)
                    else:
                        if 'VERB' in tag or 'INFN' in tag:
                            text[i] = inflection(verb, tagset, ana).word
                        else:
                            if 'PRTF' in tag:
                                text[i] = inflection(prtf, tagset, ana)
                            else:
                                if 'PRTS' in tag:
                                    text[i] = inflection(prts, tagset, ana)
                                else:
                                    if 'GRND' in tag:
                                        text[i] = inflection(grnd, tagset, ana)
                                    else:
                                        if 'NUMR' in tag:
                                            text[i] = inflection(numr, tagset, ana)
                                        else:
                                            if 'ADVB' in tag:
                                                text[i] = inflection(advb, tagset, ana)
                                            else:
                                                if 'NPRO' in tag:
                                                    text[i] = inflection(npro, tagset, ana)
                                                else:
                                                    if 'PRED' in tag:
                                                        text[i] = inflection(pred, tagset, ana)
                                                    else:
                                                        if 'PREP' in tag:
                                                            text[i] = inflection(prep, tagset, ana)
                                                        else:
                                                            if 'CONJ' in tag:
                                                                text[i] = inflection(conj, tagset, ana)
                                                            else:
                                                                if 'PRCL' in tag:
                                                                    text[i] = inflection(prcl, tagset, ana)
                                                                else:
                                                                    if 'INTJ' in tag:
                                                                        text[i] = inflection(intj, tagset, ana)
    response = text.join(' ')
    return response


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Если ты напишешь мне сообщение, я выдам тебе предложение, состоящее из таких же частей речи (наверное).")

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'
                        
@bot.message_handler(content_types = ['text'])
def send_changed(message):
    response = changewords(message)
    send_message(message.chat.id, response)

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
    
