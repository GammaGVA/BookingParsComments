from bs4 import BeautifulSoup
from time import sleep
from random import randint


def pagepars(session, params, headers) -> BeautifulSoup:
    response = session.get('https://www.booking.com/reviewlist.ru.html', params=params, headers=headers)
    soup = BeautifulSoup(response.text, features='lxml')
    if soup.find_all('div', {'class': 'c-review__row'}) != None:
        # Проверка на то, что суп вернулся не пустой.
        # Если не делать поиск то суп в любом случае не None.
        return soup
    else:
        # Если пустой, то заново перезапрос.
        sleep(randint(1, 4))
        pagepars(session, params, headers)


def pars(soup: BeautifulSoup) -> list:
    checklist = {'wifi', 'wi-fi', 'enternet', 'интернет', 'ви-фи', 'вай-фай',
                 'вайфай', 'вифи', 'интернета', 'вайфая', 'вай-фая', 'инет'}
    # Проверочные слова.
    comments = []
    all_text = soup.find_all('div', {'class': 'c-review__row'})
    # Ищу все блоки комментариев.
    if all_text:
        for txt in all_text:
            key = txt.text.lower().strip()
            key = key.replace(',', '').replace('.', '').replace('!', '').replace('?', '')
            # Переводим в нижний регистр и убираем знаки припинания.
            if set(key.split()) & checklist:
                # Проверили на пересечения/содержание ключевых слов.
                txt = txt.text.strip().replace('\xa0', ' ').replace('\r', '')
                # Убрал битовые знаки.
                comments.append(txt)
    return comments
