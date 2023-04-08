import ast
import sys

a = input()

arr = a.split(' ')

if len(arr) != 5:
    sys.exit('Некорректное выражение')

with open(r'index.json', 'r',
          encoding='utf-8') as file:
    index = ast.literal_eval(file.read())

all_values = set(range(1, 101))
all_values = set([str(i) for i in all_values])

new_arr = []

for i in range(len(arr)):
    if i % 2 == 0:
        print(arr[i])
        if arr[i].startswith('!'):
            if index.get(arr[i][1:]) is None:
                sys.exit('Слова из выражения не существуют')
            new_arr.append(all_values.difference(index.get(arr[i][1:])))
            arr[i] = arr[i][1:]
        else:
            if index.get(arr[i]) is None:
                sys.exit('Слова из выражения не существуют')
            new_arr.append(index.get(arr[i]))

if arr[1] in {'|', 'ИЛИ'}:
    if len(new_arr) < 3:
        sys.exit('Некорректное выражение')
    if arr[3] in {'|', 'ИЛИ'}:
        result = set(new_arr[0]) & set(new_arr[1]) | set(new_arr[2])
    elif arr[3] in {'&', 'И'}:
        result = set(new_arr[0]) & set(new_arr[1]) | set(new_arr[2])
elif arr[1] in {'&', 'И'}:
    if len(new_arr) < 3:
        sys.exit('Некорректное выражение')
    if arr[3] in {'|', 'ИЛИ'}:
        result = set(new_arr[0]) & set(new_arr[1]) | set(new_arr[2])
    elif arr[3] in {'&', 'И'}:
        result = set(new_arr[0]) & set(new_arr[1]) | set(new_arr[2])

if len(result) == 0:
    print("не найдено")
else:
    result = set([int(i) for i in result])
    print(sorted(result))