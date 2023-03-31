import pymorphy3
import os
import re
import io
from bisect import bisect_left
import unicodecsv as csv
morph = pymorphy3.MorphAnalyzer()
from collections import Counter

files = {}

def search(a, x, lo=0, hi=None):
    if hi is None: hi = len(a)
    pos = bisect_left(a, x, lo, hi)
    return pos if pos != hi and a[pos] == x else -1

def find(target, L):
    if L in target:
        return True
    else:
        return False


def count_words(word, file):
    l = word.lower()
    if files.get(file) is not None:
        words = files.get(file)["words"]
        return find(words, l)
    

def check_lemmas(lemma, file):
    l = lemma.lower()
    if files.get(file) is not None:
        lemmas = files.get(file)["lemmas"]

        return find(lemmas, l)


def check_word_in_files(word, files):
    documents = []
    for f in files:
        if count_words(word, f) is True:
            documents.append(f)
    return documents


def check_lemma_in_files(lemma, files):
    documents = []
    for f in files:
        if check_lemmas(lemma, f) is True:
            documents.append(f)
    return documents


def lemmatize(words, tokenized_map):
    for word in words:
        lowered = word.lower()
        if pymorphy3.MorphAnalyzer().parse(word)[0].tag.POS(lowered) not in {'INTJ', 'PRCL', 'CONJ', 'PREP'}:
            p = morph.parse(word)[0].normal_form
            arr = tokenized_map.get(p)
            if arr is None:
                new_arr = [lowered]
                tokenized_map[p] = new_arr
            else:
                arr.append(lowered)


def get_clear_words_from_file(file):
    print(file)
    with io.open(file, mode='r', encoding="utf-8") as f:
        return f.read().split('\n')
        

def get_files_from_path(path):
    arr = os.listdir(path)
    return arr