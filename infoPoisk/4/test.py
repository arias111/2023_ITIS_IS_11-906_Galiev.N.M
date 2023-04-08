# Определение множества слов-союзов
functors_pos = {'INTJ', 'PRCL', 'CONJ', 'PREP'}  # function words - предлоги и незначащие слова

# Пути к файлам
path_of_files = "tokens"
path_of_lemma_files = "lemmas"

# Пустой словарь для всех файлов
all_files_map = {}

# Бинарный поиск
def binary_search(a, x, lo=0, hi=None):
    if hi is None: hi = len(a)
    pos = bisect_left(a, x, lo, hi)                  # находит позицию для вставки
    return pos if pos != hi and a[pos] == x else -1    # не выходить за конец списка

# Функция для поиска слова в строке
def find(target, L):
    if L in target:
        return True
    else:
        return False

# Проверка наличия слова в файле
def check_word_in_file(word, file):
    l = word.lower()
    words = all_files_map.get(file)["words"]

    return find(words, l)

# Проверка наличия леммы в файле
def check_lemma_in_file(lemma, file):
    l = lemma.lower()
    lemmas = all_files_map.get(file)["lemmas"]

    return find(lemmas, l)

# Проверка наличия слова в файлах
def check_word_in_files(word, files):
    documents = []
    for f in files:
        if check_word_in_file(word, f) is True:
            documents.append(f)
    return documents

# Проверка наличия леммы в файлах
def check_lemma_in_files(lemma, files):
    documents = []
    for f in files:
        if check_lemma_in_file(lemma, f) is True:
            documents.append(f)
    return documents

# Определение части речи слова
def pos(word, morth=pymorphy3.MorphAnalyzer()):
    "Return a likely part of speech for the *word*."""
    return morth.parse(word)[0].tag.POS

# Оставить только буквы в слове
def letters(text):
    return ''.join(filter(str.isalpha, text))

# Лемматизация
def lemmatize(words, tokenized_map):
    for word in words:
        lowered = word.lower()
        if pos(lowered) not in functors_pos:
            p = morph.parse(word)[0].normal_form
            arr = tokenized_map.get(p)
            if arr is None:
                new_arr = [lowered]
                tokenized_map[p] = new_arr
            else:
                arr.append(lowered)

# Получение слов из текста
def get_clear_words(text):
    spaced_text = "".join([c if c.isalpha() else ' ' for c in text])
    words = spaced_text.split()
    clear_words = []
    for w in words:
        clear_words.append(letters(w))
    return clear_words

# Приведение всех слов к нижнему регистру
def get_words_to_lower(words):
    return [x.lower() for x in words]

# Чтение текста из файла
def read_text_from_file(file):
    with io.open(file, mode='r', encoding="utf-8") as f:
        return f.read()