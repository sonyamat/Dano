import csv
import pprint
from collections import Counter
import re

src_f = 'src.csv'
dest_f = 'dst.csv'

popul_f = 'popul.csv'
res_f = 'res2.csv'


res = []
names = []
data = {}

poselen_words = ['рабочий поселок', 'поселение', 'сельское', 'сельсовет', 'поселок', 'послок', 'село', 'рп', 'п ']
ban_words = sorted(['городское', 'район', 'муниципальный', 'пгт', 'г ', 'город', 'округ', 'городской', 'район', 'область', 'административный'], key=len, reverse=True)


def my_dist(a, b):
    def recursive(i, j):
        if i == 0 or j == 0:
            # если одна из строк пустая, то расстояние до другой строки - ее длина
            # т.е. n вставок
            return max(i, j)
        elif a[i - 1] == b[j - 1]:
            # если оба последних символов одинаковые, то съедаем их оба, не меняя расстояние
            return recursive(i - 1, j - 1)
        else:
            # иначе выбираем минимальный вариант из трех
            return 1 + min(
                recursive(i, j - 1),  # удаление
                recursive(i - 1, j),   # вставка
                recursive(i - 1, j - 1)  # замена
            )
    return recursive(len(a), len(b))

def ser_name(name):
    name = name.lower()
    name = re.sub('[^а-я ]', '', name)
    for w in poselen_words:
        name = name.replace(w, '')
    for w in ban_words:
        name = name.replace(w, '')
    # name = name.replace('ское', '')
    return name.strip()


def is_posel(name):
    for pos_w in poselen_words:
        if pos_w in name:
            return True
    for ban_w in ban_words:
        if ban_w in name:
            return False
    return True


with open(src_f) as f:
    reader = csv.DictReader(f,  delimiter=';')
    for row in reader:
        name = row['name']
        name = ser_name(name)
        if not name:
            continue

        data[name] = row['oktmo']
        names.append(name)

not_c = 0

with open(popul_f) as f:
    reader = csv.DictReader(f,  delimiter=',')
    for row in reader:
        if not is_posel(row['МО']):
            not_c += 1
            continue
        row['МО'] = ser_name(row['МО'])
        # print(row['название'])
        res.append(row)

print(not_c)

с = 0

for i in range(len(res)):
    name = res[i]['МО']
    # name = ser_name(name)
    if name is None:
        continue
    oktmo = ''
    for k, v in data.items():
        if k in name or name in k:
            oktmo = v
            # print(oktmo)
            с += 1
            break

    res[i]['октмо'] = oktmo

print(с)

with open(res_f, 'w') as f:
    wr = csv.DictWriter(f,  delimiter=';', fieldnames=['регион', 'МО', '2017', '2018', 'октмо'])
    for row in res:
        wr.writerow(row)
