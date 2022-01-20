from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request, jsonify
import nltk
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import operator
from nltk.tokenize import word_tokenize
import json
import os
import time

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# load data

#======================data cranfield for VSM============================
tfidf_file = open("./VSM/tfidf_cranfield.json", "r")
tfidf_cran = json.load(tfidf_file)

tokens_file = open("./VSM/tokens_cranfield.json", "r")
tokens_cran = json.load(tokens_file)

idfDict_file = open("./VSM/tfidf_cranfield.json", "r")
idfDict_cran = json.load(idfDict_file)


#======================data corpus for VSM===============================
tfidf_file = open("./VSM/tfidf_corpus.json", "r")
tfidf_corpus = json.load(tfidf_file)

tokens_file = open("./VSM/tokens_corpus.json", "r")
tokens_corpus = json.load(tokens_file)

idfDict_file = open("./VSM/tfidf_corpus.json", "r")
idfDict_corpus = json.load(idfDict_file)


#========================data cranfield for BIM==========================
docToken_file = open("./BIM/docToken_cranfield.json", "r")
docToken_cranfield = json.load(docToken_file)


#========================data corpus for BIM=============================
docToken_file = open("./BIM/docToken_corpus.json", "r")
docToken_corpus = json.load(docToken_file)


path_docs_cranfield = '../../cranfield/preprocessed/docs'
path_docs_corpus = '../../nfcorpus/preprocessed/docs'

listFileName_cranfield = os.listdir(path_docs_cranfield)
listFileName_cranfield = [int(fileName.split('.')[0]) for fileName in listFileName_cranfield]
listFileName_corpus = os.listdir(path_docs_corpus)
listFileName_corpus = [int(fileName.split('.')[0]) for fileName in listFileName_corpus]

def tokenize_query(query):
    tokens = nltk.word_tokenize(query)
    tokens=[x for x in set(tokens)]
    tokens=sorted(tokens)
    return tokens
def rank_BIM(query, docToken, listFileName):
    log_odd = dict.fromkeys([x for x in listFileName],0)
    query_pre = tokenize_query(query)
    for term in query_pre:
        for x in listFileName:
            try:
                log_odd[x] += docToken[str(x)][term]
            except:
                None
    log_odd = dict( sorted(log_odd.items(), key=operator.itemgetter(1),reverse=True))
    log_odd = [x for x,y in log_odd.items() if y!=0]
    return log_odd[0:10], len(log_odd)


def rank_VSM(query, tokens, idfDict, tfidf, listFileName):
    qr=nltk.word_tokenize(query)
    qr=[x for x in set(qr)]
    qrV = dict.fromkeys(tokens_cran,0)
    for word in qr:
        if word in tokens:
            qrV[word] += 1
    for words in qrV:
        try:
            qrV[words]=qrV[words]*idfDict[word]
        except KeyError:
            None
    res={}
    temp=0
    vec1=np.array([[x for x in (qrV.values())]])
    for x in listFileName:
        vec2=np.array([list(tfidf[str(x)].values())])
        if cosine_similarity(vec1,vec2) > 0:
            temp=cosine_similarity(vec1,vec2)[0][0]
            res[x]=temp
    result={}
    result = sorted(res.items(), key=operator.itemgetter(1), reverse=True)
    result = [x for x in (result)]
    if result == []:
        return [], 0
    rank=[]
    for i in range(10):
        rank.append(result[i][0])
    
    return rank, len(result)


@app.route('/search', methods=['POST'])
@cross_origin(origin='*')
def process():
    query = request.form.get('query')
    data = request.form.get('data')
    tool = request.form.get('tool')
    rank_ = []
    results = []
    nums_result = 0
    start_time = time.time()
    if query == '': 
        rank_.append('Hãy nhập từ khóa tìm kiếm')
    else:
        if(data == 'cranfield'):
            if (tool == 'VSM'):
                rank_, nums_result = rank_VSM(query, tokens_cran, idfDict_cran, tfidf_cran, listFileName_cranfield)
            else: rank_, nums_result = rank_BIM(query, docToken_cranfield, listFileName_cranfield)
            if (rank_ == []):
                rank_.append('Không tìm thấy kết quả nào cho #'+query)
            else:
                for file in rank_:
                    f_name = path_docs_cranfield + '/' + str(file) + '.txt'
                    f = open(f_name).read()
                    results.append(f)
        else:
            if(tool == 'VSM'):
                rank_, nums_result = rank_VSM(query, tokens_corpus, idfDict_corpus, tfidf_corpus, listFileName_corpus)
            else: rank_, nums_result = rank_BIM(query, docToken_corpus, listFileName_corpus)

            if (rank_ == []):
                rank_.append('Không tìm thấy kết quả nào cho #'+query)
            else:
                for file in rank_:
                    f_name = path_docs_corpus + '/' + str(file) + '.txt'
                    f = open(f_name).read()
                    results.append(f)

    end_time = time.time()
    print('time: ',end_time-start_time)
    res = [rank_, results]
    print(nums_result)
    return {
        'resuslt' : res,
        'num_res' : nums_result,
        'time' : end_time-start_time
    }
    
@app.route('/', methods=['GET'])
@cross_origin(origin='*')
def index():
  return "hello"

if __name__ == '__main__':
  app.run()
