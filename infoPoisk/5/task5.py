import math
import os
import re
import json
import operator
from sklearn.metrics.pairwise import cosine_similarity
from pymorphy2 import MorphAnalyzer

with open(r'index.json', 'r') as file:
    data = dict(json.load(file))

morph = MorphAnalyzer()
texts_directory = os.fsencode(r'texts')
doc_count = len(os.listdir(texts_directory))

def lemmatize(doc, stopwords = []):
    patterns = "[^а-яА-Я]+"
    doc = re.sub(patterns, ' ', doc)
    tokens = []
    for token in doc.split():
        if token and token not in stopwords:
            token = token.strip()
            token = morph.normal_forms(token)[0]
            tokens.append(token)
    if len(tokens) > 0:
        return tokens
    return None

def get_url(index):
    with open(r'index.txt', 'r', encoding='utf-8') as file:
        data = file.readlines()
    result = None
    for file in data:
        num = file.split(" -> ")[0].split(".")[0]
        url = file.split(" -> ")[1][:-1]
        if str(num) == str(index):
            result = url
    return result

def query_tf_idf(token, query):
    try:
        doc_with_token_count = len(data.get(token))
    except:
        return 0
    q_tf = query.count(token) / len(query)
    q_idf = math.log(doc_count / doc_with_token_count)
    return round(q_tf * q_idf, 6)

def search(query):
    query = lemmatize(query)

    query_vector = []

    for token in query:
        query_vector.append(query_tf_idf(token, query))

    vectors_distances = {}

    for file in os.listdir(texts_directory):
        index = file.decode("utf-8").split('.')[0]

        document_vector = []

        for token in query:
            try:
                tf_idf = data.get(token).get(index).get("TF-IDF")
                document_vector.append(tf_idf)
            except:
                document_vector.append(0.0)

        vectors_distances[index] = cosine_similarity([query_vector], [document_vector])[0][0]


    searched_indices = sorted(vectors_distances.items(), key=operator.itemgetter(1), reverse=True)

    for index in searched_indices:
        doc_id, tf_idf = index

        url = get_url(doc_id)
        print("Индекс: {}  Косинус:{}".format(doc_id, tf_idf))

search(input())

#Статьи Список Интервью
#Цена Обработка Персональных