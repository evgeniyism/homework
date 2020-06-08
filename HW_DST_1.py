from bs4 import BeautifulSoup
import requests
from time import sleep
import pandas as pd
import numpy as np

links = []

for page in range(1,10):
    url = f'https://www.kinopoisk.ru/lists/top250/?page={str(page)}&sort=popularity&tab=all'
    r = requests.get(url)
    sleep(60)
    soup = BeautifulSoup(r.text, 'lxml')
    films = soup.findAll('div', class_='desktop-rating-selection-film-item')
    for i in films:
        link = 'https://www.kinopoisk.ru' + i.find('div', class_='selection-film-item-meta selection-film-item-meta_theme_desktop').find('a').get('href')
        print(link)
        links.append(link)

print(links)

file = open('links.csv', 'w')
file.write(str(links))
file.close()

clean_links = []

with open('links.csv', 'r') as links:
    links = links.readlines()
    for i in links:
        new_line = i.strip().replace('[','').replace(']','').replace('\n','').replace('п»ї','')
        clean_links.append(new_line)

df = pd.DataFrame(columns=['Название', 'Kinopoisk', 'IMDB'])
counter = 1

for url in clean_links:
    r = requests.get(url)
    print(f'Делаю запрос к {url}, шаг {counter}')
    counter +=1
    rand = np.random.randint(1, high=59, size=None, dtype='l')
    sleep(300+rand)
    soup = BeautifulSoup(r.text, 'lxml')
    try:
        kp_score = soup.find('div', class_='div1').find('meta').get('content')
        imdb_score = soup.find('div', style="color:#999;font:100 11px tahoma, verdana").text[6:10]
        movie_name = soup.find('span', class_='moviename-title-wrapper').text
        movie_item = {'Название': movie_name, 'Kinopoisk': kp_score, 'IMDB': imdb_score}
        print(f'Получено {movie_item}')
        try:
            if movie_item['Kinopoisk'].replace('.', '').isnumeric():
                df = df.append(pd.DataFrame.from_dict([movie_item]), ignore_index=True)
                df.to_csv('final_file_kp.csv', ',', index=False, encoding='cp1251')
                print(f'{movie_item} записан в файл')
                success = f'{counter}. сделан успешный запрос к {url}\n'
                with open('parser_log.txt', 'a') as log:
                    log.write(success)
        except:
            fail = f'{counter}. Произошла ошибка, ссылка {url}\n'
            print(fail)
            with open('parser_log.txt', 'a') as log:
                log.write(fail)
    except:
        fail = f'{counter} Произошла ошибка, ссылка {url}\n'
        print(fail)
        with open('parser_log.txt', 'a') as log:
            log.write(fail)
        sleep(60)
