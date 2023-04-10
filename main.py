import requests
from params_headers import params, headers
from random import randint
from page_pars import pars, pagepars

Referer = input('Введите url отеля: ')
# Запрашиваем ссылку
headers['Referer'] = Referer
# Говорим что мы с неё и переходим

cc1 = Referer.split('/')[4]
params['cc1'] = cc1
# Добавляем параметр cc1

pagename = Referer.split('/')[5].split('.')[0]
params['pagename'] = pagename
# Добавляем параметр pagename, он самы основной тут.

points = Referer.split('?')[1]  # Отберём параметры.
points = points.split('&')[:-1]  # Последний элементы мусорный.

xuz = lambda: f'16809{randint(0, 99999999):08}'  # Не знаю что это, но у него 16809 не изменно и далее 8 цифр меняются.
# Без него/с любым значением работает, решил оставить в таком виде. Вызывается в параметрах.
params['_'] = xuz()
# Добавляем параметр _

if len(points) == 4:
    # Ссылка может состоять двумя видами. Либо 4 элемента и в 4 вся инфа.
    aid = points[0].split('=')[1]
    params['aid'] = aid
    headers['aid'] = aid
    # Добавляем параметр и заголовок aid

    label = points[1].split('=')[1]
    params['label'] = label
    headers['label'] = label
    # Добавляем параметр и заголовок label

    sid = points[2].split('=')[1]
    params['sid'] = sid
    # Добавляем параметр sid

    srpvid = points[3].split(';')[-3].split('=')[1]
    params['srpvid'] = srpvid
    # Добавляем параметр srpvid

else:
    # Либо Много элементов и могут быть в перемешку.
    for p in points:
        pp = p.split('=')
        if pp[0] == 'aid':
            aid = pp[1]
            params['aid'] = aid
            headers['aid'] = aid
            # Добавляем параметр и заголовок aid
        elif pp[0] == 'label':
            label = pp[1]
            params['label'] = label
            headers['label'] = label
            # Добавляем параметр и заголовок label
        elif pp[0] == 'sid':
            sid = pp[1]
            params['sid'] = sid
            # Добавляем параметр sid
        elif pp[0] == 'srpvid':
            srpvid = pp[1]
            params['srpvid'] = srpvid
            # Добавляем параметр srpvid

session = requests.Session()
# Скорее всего Session лишнее, работает и без него. Но решил перебдеть.
# Так как я не передают конкретные печеньки(протухнут спустя время), решил использовать сессию.
# На просторах Ру-нета читал не однократно, что сессия генирирует печеньки.
soup = pagepars(session=session, headers=headers, params=params)
maxnumberpage = int(soup.find_all('span', {'class': 'bui-u-sr-only'})[-1].text.split()[-1])  # Кол-во страниц
comments = pars(soup=soup)  # Парсим первую страницу
print(f'1/{maxnumberpage}')

if maxnumberpage > 1:  # Если страниц больше 1, то парсим все остальные.
    for numberpage in range(2, maxnumberpage + 1):
        print(f'{numberpage}/{maxnumberpage}')
        params['offset'] = numberpage * 10
        params['_'] = xuz()
        soup = pagepars(session=session, headers=headers, params=params)
        comment = pars(soup=soup)
        comments += comment

print(*comments, sep="\n")
