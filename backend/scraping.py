from json import dumps
from time import time
from multiprocessing import Pool
from mureq import get, Response, HTTPException
from bs4 import BeautifulSoup

class AdditiveScrap:
    def __init__(self): 
        self._dangerlvls_list: list[str] = self._get_dangerlvls_list()
        self._categories_list: list[str] = self._get_categories_list()
        self._origins_list:    list[str] = self._get_origins_list()
        self._origins_list.append('Атмосферные газы')
        self._additive_list:   list[str] = self._get_additive_list()

    def _get_categories_list(self) -> list[str]:
        url: str = "https://proe.info/ru/additives/krasiteli"

        response: Response = get(url=url)
        categories_list: list[str] = [item.text.strip() for item in BeautifulSoup(response.body, 'lxml')
                                    .find(name= 'ul', class_= 'hierarchical-taxonomy-menu')
                                    .find_all(name= 'a', class_= 'block-taxonomymenu__link')
                                    ]
        return categories_list

    def _get_dangerlvls_list(self) -> list[str]:
        url: str = "https://proe.info/ru/additives"

        response: Response = get(url=url)
        dangerlvls_list: list = [item.text.strip() for item in BeautifulSoup(response.body, 'lxml')
                                    .find(name= 'div', class_= 'spoiler')
                                    .find(name= 'div', class_= 'view-id-additives_legend')
                                    .find_all(name= 'h3', class_= 'term--additive-dangers')
                                    ]
        return dangerlvls_list

    def _get_origins_list(self) -> list[str]:
        url: str = "https://proe.info/ru/additives"

        response: Response = get(url=url)
        dangerlvls_list: list = [item.text.strip() for item in BeautifulSoup(response.body, 'lxml')
                                    .find(name= 'div', class_= 'spoiler')
                                    .find(name= 'div', class_= 'view-id-additives_legend')
                                    .find_all(name= 'h3', class_= 'term--additive-origins')
                                    ]
        return dangerlvls_list

    # Функция собирает ссылки из определённых объектов страницы в список
    def _get_additive_list(self) -> list[str]:
        url: str = "https://proe.info/ru/additives"

        # Получение страниц
        response_part1: Response = get(url=url, params= {'page':'0'})
        response_part2: Response = get(url=url, params= {'page':'1'})

        adds_list: list[str] = []

        # Вычленение тегов из html-страниц по css-классам
        adds_list += [item['href'] for item in BeautifulSoup(response_part1.body, 'lxml').find_all(name= 'a', class_= 'addicon__link')]
        adds_list += [item['href'] for item in BeautifulSoup(response_part2.body, 'lxml').find_all(name= 'a', class_= 'addicon__link')]

        return adds_list

    def _local_additives_json(self, link):
        self._save_to_json(self._get_one_additive(link= link))

    # Функция сохранения в JSON файлы по пути ./eshki
    def _save_to_json(self, eshka):
        try:
            template: str = dumps({
                'e_id': eshka['e_id'],
                'name': eshka['name'],
                'danger_level': eshka['danger_level'],
                'e_type': eshka['e_type'],
                'origins': eshka['origins'],
                'description': eshka['description']
            }, ensure_ascii=False)

            with open(f'./eshki/dobavka{eshka['e_id']}.json', 'w', encoding='utf-8') as file:
                file.write(template)
        except Exception as err:
            print(err, '' 'Ошибка в сохронении', eshka)

    def _get_one_additive(self, link: str):
        try:
            url: str = f"https://proe.info{link}"
            response: Response = get(url=url)
            soup = BeautifulSoup(response.body, 'lxml').find(name= 'div', class_= 'region--content')
            e_id: str = soup.find(name= 'div', class_='addicon__name').text
            name: str = soup.find(name= 'span', class_= 'field--title').text
            danger_level: str = self._dangerlvls_list.index(soup.find(name= 'div', class_='addprop--danger'
                                    ).find(name= 'a', class_= 'addprop-item'
                                    ).text)
            e_type: list[str] = [self._categories_list.index(item.string) for item in soup.find(name= 'div', class_='addprop--category'
                                    ).find_all(name= 'a', class_= 'addprop-item')]
            origins: list[str] =  [self._origins_list.index(origin.string) for origin in (soup.find(name= 'div', class_='addheader__right-top').find_all('a'))]
            description: str = soup.find(name= "div", class_='field--additive-info'
                                    ).find('p'
                                    ).text
            return ({
                'e_id' : e_id,
                'name' : name, 
                'danger_level' : danger_level, 
                'e_type' : e_type, 
                'origins' : origins, 
                'description' : description
                })
        except HTTPException as err:
            return {
                'error' : err,
                'url' : url
            }
        except Exception as err:
            return {
                'error' : err,
                'desc'  : f'Ошибка в получении данных, {link}'
            }

    # Функция запуска сбора данных из добавок: 20 процессов на 20 добавок
    def _get_additives_data(self):
        try:
            with Pool(20) as p:
                p.map(self._local_additives_json, self._additive_list)
        except Exception as err:
            print(err, '', 'Ошибка в многопоточке')

    def __call__(self):
        start_time = time()
        self._get_additives_data()
        print("--- %s seconds ---" % (time() - start_time))


if __name__ == '__main__':
    
    obj = AdditiveScrap()
    obj()
    print(callable(obj))