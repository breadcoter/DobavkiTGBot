from json import dumps
from time import time
from multiprocessing import Pool
from mureq import get, Response
from bs4 import BeautifulSoup

# Функция собирает ссылки из определённых объектов страницы в список
def get_adictives_list() -> list[str]:
    url: str = "https://proe.info/ru/additives"

    # Получение страниц
    response_part1: Response = get(url=url, params= {'page':'0'})
    response_part2: Response = get(url=url, params= {'page':'1'})

    adds_list: list[str] = []

    # Вычленение тегов из html-страниц по css-классам
    adds_list += [item['href'] for item in BeautifulSoup(response_part1.body, 'lxml').find_all(name= 'a', class_= 'addicon__link')]
    adds_list += [item['href'] for item in BeautifulSoup(response_part2.body, 'lxml').find_all(name= 'a', class_= 'addicon__link')]

    return (adds_list)

def get_one_adict(link: str):
    url: str = f"https://proe.info{link}"
    response: Response = get(url=url)
    soup = BeautifulSoup(response.body, 'lxml').find(name= 'div', class_= 'region--content')
    e_id: str = soup.find(name= 'div', class_='addicon__name').text
    name: str = soup.find(name= 'span', class_= 'field--title').text
    danger_level: str = soup.find(name= 'div', class_='addprop--danger'
                            ).find(name= 'a', class_= 'addprop-item'
                            ).text
    e_type: list[str] = [item.string for item in soup.find(name= 'div', class_='addprop--category'
                            ).find_all(name= 'a', class_= 'addprop-item')]
    origins: list[str] =  [origin.string for origin in (soup.find(name= 'div', class_='addheader__right-top').find_all('a'))]
    description: str = soup.find(name= "div", class_='field--additive-info'
                            ).find('p'
                            ).text

    template: str = dumps({
        'e_id': e_id,
        'name': name,
        'danger_level': danger_level,
        'e_type': e_type,
        'origins': origins,
        'description': description
    }, ensure_ascii=False)

    with open(f'./eshki/dobavka{e_id}.json', 'w', encoding='utf-8') as file:
        file.write(template)

def get_adicives_data():
    adicts_links: list[str] = get_adictives_list()
    with Pool(20) as p:
        p.map(get_one_adict, adicts_links)

if __name__ == '__main__':
    start_time = time()
    get_adicives_data()
    print("--- %s seconds ---" % (time() - start_time))