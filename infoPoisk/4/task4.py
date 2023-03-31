import math
import pymorphy3
import io
import re
from bisect import bisect_left
import unicodecsv as csv
import methods

morph = pymorphy3.MorphAnalyzer()
from collections import Counter

all_files = {}

def get_lemma_file_by_token_file(file):
    file_index = int(re.search(r'\d+', file).group())
    found = None
    for f in lemma_files:
        if re.search(r'\d+', f) is not None:
            f_index = int(re.search(r'\d+', f).group())
            if f_index == file_index:
                found = f
                break
    return found


files = methods.get_files_from_path("tokens/")
lemma_files = methods.get_files_from_path("lemmas/")

for f in files:
    if f != '.DS_Store':
        tokenized_map = {}

        words = methods.get_clear_words_from_file(f)

        lemma_file = get_lemma_file_by_token_file(f)
        lemmas = methods.get_clear_words_from_file(lemma_file)
        all_files[f] = {}
        all_files[f]["words"] = methods.get_words_to_lower(words)
        all_files[f]["lemmas"] = methods.get_words_to_lower(lemmas)


for f in files:
    print(f)
    if f != '.DS_Store':
        tokenized_map = {}

        words = all_files[f]["words"]
        lemmas = all_files[f]["lemmas"]
        methods.lemmatize(words, tokenized_map)

        total_token_count = len(words)
        c = Counter(words)
        uniq_token = c.keys()

        with io.open("tokensTf/tf" + f + ".csv", 'w', encoding="utf-8") as tff:
            t_str = "TOKEN;TF;IDF;TF*IDF"
            tff.write(f"{t_str}\n")
            for t in uniq_token:
                tf = round((c[t] / total_token_count), 6)
                document_count_for_t = methods.check_word_in_files(t, files)
                idf = round(math.log2(len(files) / len(document_count_for_t)), 6)
                tf_idf = round(tf * idf, 6)
                t_str = f"{t};{tf};{idf};{tf_idf}"
                tff.write(f"{t_str}\n")

        lemmas_count = len(tokenized_map.keys())

        with io.open("lemmaTf/lemma" + f + ".csv", 'w', encoding="utf-8") as tff:
            t_str = "LEMMA;TF;IDF;TF*IDF"
            tff.write(f"{t_str}\n")
            for l in lemmas:
                tf = round(len(tokenized_map[l]) / lemmas_count,6)
                document_count_for_l = methods.check_lemma_in_files(l, files)
                idf = round(math.log2(len(files) / len(document_count_for_l)),6)
                tf_idf = round(tf * idf, 6)
                t_str = f"{l};{tf};{idf};{tf_idf}"
                tff.write(f"{t_str}\n")