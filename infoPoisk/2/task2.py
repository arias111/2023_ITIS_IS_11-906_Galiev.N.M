import pymorphy3  # библиотека, которая может взять начальную форму слов
import glob
import io
import os

morph = pymorphy3.MorphAnalyzer()

# CONJ- союз
# INTJ- междометие
functors_pos = {'INTJ', 'PRCL', 'CONJ', 'PREP'}  # function words - предлоги и незначащие слова
path_of_files = "texts/"


def pos(word, morth=pymorphy3.MorphAnalyzer()):
    "Return a likely part of speech for the *word*."""
    return morth.parse(word)[0].tag.POS


def letters(text):
    return ''.join(filter(str.isalpha, text))


def lemmatize(words, tokenized_map):
    for word in words:
        if pos(word) not in functors_pos:
            p = morph.parse(word)[0].normal_form
            arr = tokenized_map.get(p)
            if arr is None:
                new_arr = set()
                new_arr.add(word)
                tokenized_map[p] = new_arr
            else:
                arr.add(word)


def get_clear_words(text):
    # Заменяем все символы на пробел, если это не буква
    spaced_text = "".join([c if c.isalpha() else ' ' for c in text])
    words = spaced_text.split()
    clear_words = []
    for w in words:
        clear_words.append(letters(w))
    return clear_words


def read_text_from_file(file):
    with io.open(file, mode='r', encoding="utf-8") as f:
        return f.read()


def get_files_from_path(path):
    arr = os.listdir(path)
    return arr

files = get_files_from_path(path_of_files)
for f in files:
    print(f)
    if f > '0':
        text = read_text_from_file(path_of_files + f)
        words = get_clear_words(text)
        tokenized_map = {}
        lemmatize(words, tokenized_map)

        all_tokens = tokenized_map.values()
        with io.open('tokens/tokens_' + str(f), 'w', encoding="utf-8") as ff:
            # all_tokens = np.array(all_tokens)
            all_tokens =  [item for sublist in all_tokens for item in sublist]
            # all_tokens = list(all_tokens.split('\n'))
            all_tokens.sort()
            print(all_tokens)
            for t in all_tokens:
               ff.write(f"/{t}\n")

        with io.open('lemmas/lemmas_' + str(f), 'w', encoding="utf-8") as ff:
            items = tokenized_map.items()
            items = sorted(items)
            for lemma, tokens in items:
                ff.write(f"{lemma}\n")


