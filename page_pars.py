from bs4 import BeautifulSoup
from time import sleep
from random import randint
from translate import Translator


def pagepars(session, params, headers, key_out=3) -> BeautifulSoup:
    response = session.get('https://www.booking.com/reviewlist.ru.html', params=params, headers=headers)
    soup = BeautifulSoup(response.text, features='lxml')
    if soup.find_all('div', {'class': 'c-review__row'}) != None:
        # Проверка на то, что суп вернулся не пустой.
        # Если не делать поиск, то суп в любом случае не None.
        return soup
    else:
        # Если пустой, то заново перезапрос.
        if key_out:
            sleep(randint(1, 4))
            key_out -= 1
            pagepars(session, params, headers, key_out=key_out)
        else:
            print('Страницу пропустили.')
            return None



def pars(soup: BeautifulSoup) -> list:
    checklist = {'wifi', 'wi-fi', 'enternet', 'интернет', 'ви-фи', 'вай-фай',
                 'вайфай', 'вифи', 'интернета', 'вайфая', 'вай-фая', 'инет'}
    # Проверочные слова.
    translator = Translator(to_lang='ru')
    comments = []
    all_text = soup.find_all('div', {'class': 'c-review__row'})
    # Ищу все блоки комментариев.
    if all_text:
        for txt in all_text:
            txt = txt.text.strip().replace('\xa0', ' ').replace('\r', ' ').replace('·', ':').split()
            txt = ' '.join(txt)
            # Убрал битовые знаки и лишние пробелы.
            key = txt.lower().replace(',', ' ').replace('.', ' ').replace('!', ' ').replace('?', ' ')
            # Переводим ключ в нижний регистр и убираем знаки препинания.
            if set(key.split()) & checklist:
                # Проверили на пересечения/содержание ключевых слов.
                transtxt = translator.translate(txt)
                # Перевели комментарии на русский какие смогли, что-то не переводи, что-то переводит частично.
                # googletrans хуже, переводит меньше, медленнее и ошибки лезут постоянно из-за символов в тексте.
                if not transtxt.startswith('MYMEMORY WARNING') and len(txt) < 500:
                    # Может закончиться полторачасовой лимит либо много символов в тексте.
                    txt = transtxt
                comments.append(txt)
    return comments
