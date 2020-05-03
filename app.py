#import library yang dibutuhkan
from flask import Flask,render_template,request
import math #untuk orepasi matematika
import numpy as np #untuk orepasi vektor
from scipy import spatial

app = Flask(__name__)

# memproses query untuk diseleksi dan disimpan ke array (dari input user)

def process_query (current_list):
	new_list = []
	for word in current_list:
		if word in closed_class_stop_words:
			continue
		if word.isalnum() == False:
			continue
		if word.isdigit():
			continue
		if word not in new_list:
			new_list.append(word)
            
	query.append(new_list)

# memproses query untuk diseleksi dan disimpan ke array (dari dokumen query)
def process (current_list):
	new_list = []
	for word in current_list:
		if word in closed_class_stop_words:
			continue
		if word.isalnum() == False:
			continue
		if word.isdigit():
			continue
		if word not in new_list:
			new_list.append(word)
	query_text.append(new_list)

# memproses dokumen(1400 dokumen)
def process2 (current_list, abstract_index):

	new_list = [] #untuk menyimpan list kata
	for word in current_list:
		if word in closed_class_stop_words:
			continue
		if word.isalnum() == False:
			continue
		if word.isdigit():
			continue
		if word not in new_list:
			new_list.append(word) #input kata ke list
        
        #membuat index kumpulan kata 
        #misal kata similarity dia ada di dokumen mana aja dan muncul berapa kali didokumen itu
		if word not in abstract_words:
			abstract_words[word] = {}
		abstract_words[word][abstract_index] = abstract_words[word].get(abstract_index, 0.0) + 1
        
    #menyimpan jumlah dokumen yang mengandung kata x
	for word in new_list:
		abstract_words[word]['SUM'] = abstract_words[word].get('SUM', 0.0) + 1

abstract_words = {} #tipe data dictionery
query_text = [] #tipe data array
query = [] #tipe data array

closed_class_stop_words = ['a','the','an','and','or','but','about','above','after','along','amid','among',\
                           'as','at','by','for','from','in','into','like','minus','near','of','off','on',\
                           'onto','out','over','past','per','plus','since','till','to','under','until','up',\
                           'via','vs','with','that','can','cannot','could','may','might','must',\
                           'need','ought','shall','should','will','would','have','had','has','having','be',\
                           'is','am','are','was','were','being','been','get','gets','got','gotten',\
                           'getting','seem','seeming','seems','seemed',\
                           'enough', 'both', 'all', 'your' 'those', 'this', 'these', \
                           'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my',\
                           'its', 'his' 'her', 'every', 'either', 'each', 'any', 'another',\
                           'an', 'a', 'just', 'mere', 'such', 'merely' 'right', 'no', 'not',\
                           'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more',\
                           'most', 'less' 'least', 'so', 'enough', 'too', 'pretty', 'quite',\
                           'rather', 'somewhat', 'sufficiently' 'same', 'different', 'such',\
                           'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which',\
                           'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace', \
                           'anything', 'anytime' 'anywhere', 'everybody', 'everyday',\
                           'everyone', 'everyplace', 'everything' 'everywhere', 'whatever',\
                           'whenever', 'whereever', 'whichever', 'whoever', 'whomever' 'he',\
                           'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their','theirs',\
                           'you','your','yours','me','my','mine','I','we','us','much','and/or'
                           ]

#memproses query
f = open('cran.qry', 'r') #membuka file cran.qry(file kumpulan query)
current_list = []

for line in f:
	string_list = line.split()
	if string_list[0] == '.I':
		if current_list != []:
			process (current_list)
			current_list = []
	elif string_list[0] == '.W':
		continue
	else:
		current_list += string_list

process (current_list)
f.close()

#memproses dokumen
f = open('cran.all.1400', 'r')
current_list = []
abstract_index = -1

for line in f:
	string_list = line.split()
	if string_list[0] == '.I':
		first_w = True
		if current_list != []:
			process2 (current_list, abstract_index)
		abstract_index += 1

	elif string_list[0] == '.W':
		if (first_w == True):
			current_list = []
			first_w = False 
	else:
		current_list += string_list

process2 (current_list, abstract_index)
f.close()

@app.route('/')
def dokumen():
    dokumen = open('cran.all.1400','r')
    isi = dokumen.readlines()

    dokumen.close()
    return render_template('index.html',isi=isi)

@app.route('/query')
def dokumen_query():
    query = open('cran.qry','r')
    isi = query.readlines()
    query.close()
    return render_template('query.html',isi=isi)

@app.route('/relevant')
def dokumen_relevant():
    relevant = open('cranqrel','r')
    isi = relevant.readlines()
    relevant.close()
    return render_template('relevant.html',isi=isi)

@app.route('/hasilsistem')
def hasil_sistem():
    # menghitung sim dari setiap query yang ada
    f = open('outputIRSistem.txt', 'w')
    for i in range (226):
        abstract_similarity = []
        for j in range (1405):
            abstract_score = []
            row_tf = []
            for word in query_text[i]:
                if word not in abstract_words:
                    tf = 0.0
                    idf = 0.0
                else:
                    tf = abstract_words[word].get(j, 0.0)
                    idf = math.log10(1405.0/abstract_words[word]['SUM'])
                if(tf > 0):
                    abstract_score.append(1*(idf+1))
                else:
                    abstract_score.append(0*(idf+1))
                row_tf.append(tf)
            simfix = np.dot(row_tf,abstract_score)
                
    #		for sim in abstract_score:
    #			simfix += sim
            abstract_similarity.append(simfix)

        abstract_similarity_index = sorted(range(len(abstract_similarity)), \
            key = lambda k: abstract_similarity[k], reverse = True)
        abstract_similarity.sort(reverse = True)

        for j in range (1405):
            query_num = str(i+1)
            abstract_num = str(abstract_similarity_index[j] + 1)
            similarity = '{0:.15f}'.format(abstract_similarity[j])
            if i == 0 and j == 0:
                f.write(query_num + ' ' + abstract_num + ' ' + similarity)
            else: 
                f.write('\n' + query_num + ' ' + abstract_num + ' ' + similarity)

    f.close()

    relevant_sistem = open('hasilIRSistem.txt','r')
    isi = relevant_sistem.readlines()
    relevant_sistem.close()
    return render_template('hasilsistem.html',isi=isi)

@app.route('/queryuser',methods=['GET','POST'])
def query_user():
    #menampilkan hasil pencarian pengguna
    inputan = ""
    if request.method=="POST":
        inputan = request.form['query']
    current_list = []
    current_list = inputan.split()
    new_list = []
    query = []
    for word in current_list:
        if word in closed_class_stop_words:
            continue
        if word.isalnum() == False:
        	continue
        if word.isdigit():
            continue
        if word not in new_list:
            new_list.append(word.lower())  
    query.append(new_list) #menyimpan query dalam query

    #proses pencarian dan memberi index
    for i in range (1):
        abstract_similarity = []
        for j in range (1405):
            abstract_score = []
            row_tf = []
            for word in query[i]:
                if word not in abstract_words:
                    tf = 0.0
                    idf = 0.0
                else:
                    tf = abstract_words[word].get(j, 0.0)
                    idf = math.log10(1405.0/abstract_words[word]['SUM'])
                if(tf > 0):
                    abstract_score.append(1*(idf+1))
                else:
                    abstract_score.append(0*(idf+1))
                row_tf.append(tf)
            simfix = np.dot(row_tf,abstract_score)
            abstract_similarity.append(simfix)

        abstract_similarity_index = sorted(range(len(abstract_similarity)), \
            key = lambda k: abstract_similarity[k], reverse = True)
        abstract_similarity.sort(reverse = True)
        jumlah_hasil=0    
        for j in range (1405):
            similarity = abstract_similarity[j]
            if similarity == 0:
                continue
            else: 
                jumlah_hasil += 1
        print(query)

    return render_template('queryuser.html',hasil=jumlah_hasil,index=abstract_similarity_index,sim=abstract_similarity,query=inputan)

@app.route('/hasil/<index>',methods=['GET','POST'])
def coba(index):
    isihasil = []
    tanda = False
    c = 0
    if request.method=="POST":
        c = request.form["index"]
    else:
        c = index
    text = open('cran.all.1400','r')
    for line in text:
        isitext = line.split()
        if isitext == ['.I',str(c)]:
            tanda = True
            print (isitext)
        elif isitext == ['.I',str(int(c)+1)]:
            tanda = False

        if tanda == True:
            isihasil.append(line)
            
    return render_template('hasil.html',isihasil=isihasil, index=index)
