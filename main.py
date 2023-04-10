import requests
from bs4 import BeautifulSoup
from random import randint
from page_pars import pars, pagepars

Referer = input('Введите url отеля: ')

cc1 = Referer.split('/')[4]
pagename = Referer.split('/')[5].split('.')[0]

points = Referer.split('?')[1]  # Отберём параметры.
points = points.split('&')[:-1]  # Последний элементы мусорный.

xuz = lambda: f'16809{randint(0, 99999999):08}'  # Не знаю что это, но у него 16809 не изменно и далее 8 цифр меняются.
# Без него/с любым значением работает, решил оставить в таком виде. Вызывается в параметрах.
params = {
    'cc1': cc1,
    'pagename': pagename,
    'r_lang': '',
    'review_topic_category_id': '',
    'type': 'total',
    'score': '',
    'sort': '',
    'time_of_year': '',
    'dist': '1',
    'rows': '10',
    'rurl': '',
    'text': '',
    'translate': '',
    '_': xuz(),
    'offset': '0',
}

if len(points) == 4:
    # Ссылка может состоять двумя видами. Либо 4 элемента и в 4 вся инфа.
    aid = points[0].split('=')[1]
    params['aid'] = aid
    label = points[1].split('=')[1]
    params['label'] = label
    sid = points[2].split('=')[1]
    params['sid'] = sid

    srpvid = points[3].split(';')[-3].split('=')[1]
    params['srpvid'] = srpvid

else:
    # Либо Много элементов и могут быть в перемешку.
    for p in points:
        pp = p.split('=')
        if pp[0] == 'aid':
            aid = pp[1]
            params['aid'] = aid
        elif pp[0] == 'label':
            label = pp[1]
            params['label'] = label
        elif pp[0] == 'sid':
            sid = pp[1]
            params['sid'] = sid
        elif pp[0] == 'srpvid':
            srpvid = pp[1]
            params['srpvid'] = srpvid



headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': Referer,
    # 'X-Booking-Pageview-Id': 'f009613c05ef0028',
    'X-Booking-AID': aid,
    # 'X-Booking-Session-Id': 'bd39711fc1a63b79c5158345408ed521',
    'X-Booking-SiteType-Id': '1',
    'X-Partner-Channel-Id': '17',
    'X-Booking-Label': label,
    # 'X-Booking-CSRF': 'OKkxZAAAAAA=y-oXJ2hT2YTa4QclcTYweXWq1rzHc6JtqtPnHRHmNkRDk1x5fHb8mClOnrV2pSH5fsbf6nnOfZuWceF-CUTIBDjlO1-2zE7l4Ssk9atPdC1f_5v6CCeftEgD6kjrr62d6p-KcHuLWoDkdaQer_Q0cbKtWzlN6P96UHCkBmK8QHKcFDS-Olhy0kqitexx4oTTU5lxjEKLzAkyFsVA',
    'X-Booking-Language-Code': 'ru',
    'X-Booking-Client-Info': 'THHSOFRURURYNYHIYTLRQJRbWdWOGVO|1,THHSOFRURURYNYHIYTLRQJRbWdWOGVO|3,THHSOFRURURYNYHIYTLRQJRbWdWOGVO|5,eWHMYTBADDbdEBVTQWUVIZdRRT|1,eWHMYTBADDbdEBVTQWUVIZdRRT|2,aaTBNZZJRLESPIDNJDPVBC|1,aaTBNZZJRLESPIDNJDPVBC|3,THHSODPNGZfSeUNAFQEGRDDNC|1,adUAAVfDfWZJEHSCGVbSHT|1,adUAAVfDfWZJEHSCGVbSHT|3',
    'X-Booking-Info': '1484870,1696800,1699500,1699930,1703010,1703190,1706090,1707990,1708660,1709210,1710150,1710740,1710950,1714370,1715410,THHSOFRURURYNYHIYTLRQJRbWdWOGVO|1,1703190|1,1703190|4,1710150|4,1707990|1,1710150|2,1699930|2,1698510|1,1714160|1,1696800|3,THHSOFRURURYNYHIYTLRQJRbWdWOGVO|3,THHSOFRURURYNYHIYTLRQJRbWdWOGVO|5,eWHMYTBADDbdEBVTQWUVIZdRRT|1,eWHMYTBADDbdEBVTQWUVIZdRRT|2,aaTBNZZJRLESPIDNJDPVBC|1,ADDbdEBAHUNHefKbAXSIZIBLGEXO|1,ADDbdEBAHUNHefKbAXSIZIBLGEXO|2,NAFLeOeJAETbMHVVXFQbMDZOKPWZJae|2,NAFLeOeJAETbMHVVXFQbMDZOKPWZJae|4,NAFLeOeJAETbMHVVXFQbMDZOKPWZJae|5,NAFLeOeJAdcbdGTEYOdDWBLHMVC|1,NAFLeOeJAdcbdGTEYOdDWBLHMVC|2,INFddKNKNKPBDJJHMVGPLTLReASdVLT|2,aaTBNZZJRLESPIDNJDPVBC|3,THHSODPNGZfSeUNAFQEGRDDNC|1,adUAAVfDfWZJEHSCGVbSHT|1,HINZJLeUXSaZbOTMXC|1,HINZJLeUXSaZbdKNKNKPJdBJOTXNORe|1,HINZJLeUXSaZbOTMXC|2,HINZJLeUXSaZbOTMXC|6,HINZJLeUXSaZbOTMXC|4,YdXfMTXEUDdeOYSCaIfWcACVVLZPecOEO|1,YdXfMTXEUDdeOYSCaIfWcACVVLZPecOEO|3,OOGbIFBUEDUJfYcPBPUObeZFZVTHT|1,OOGbIFBUbTdNDNQJYBXe|1,eWHMcCcCcCFKJBKWUbPNadSFbTdNDNSNC|1,eWHMADDbdEcLcDNTVXVGMVXATRDJbfMRTKe|1,ADDbdEBAHUNHefKbAXSIZIBLGEXO|3,ADDbdEBAHUNHefKbAXSIZIBLGEXO|4,ADDbdEBAHUNHefKbAXSIZIBLGEXO|5,aXBNTfZHYHQDVCXdUFDeTQQVDaVYEO|1,aXBNTfZHYHQDVCXdUFDeTQQVDaVYEO|3,adUAAVfDfWZJEHSCGVbSHT|3',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}
# Оставил комментариями те данные, которые динамические. Другие длинные не менялись.


session = requests.Session()
# Скорее всего Session лишнее, работает и без него. Но решил перебдеть.
# Так как я не передают конкретные печеньки(протухнут спустя время), решил использовать сессию.
# На просторах Ру-нета читал не однократно, что сессия генирирует печеньки.
soup = pagepars(session=session, headers=headers, params=params)
maxnumberpage = int(soup.find_all('span', {'class': 'bui-u-sr-only'})[-1].text.split()[-1])
comments = pars(soup=soup)

if maxnumberpage > 1:
    for numberpage in range(2, maxnumberpage + 1):
        print(f'{numberpage}/{maxnumberpage}')
        params['offset'] = numberpage * 10
        params['_'] = xuz()
        soup = pagepars(session=session, headers=headers, params=params)
        a = pars(soup=soup)
        comments += a

for comment in comments:
    print(comment)
