import json

import requests


def get_category(category):
    """Функция, находящая категории, в которых присутствует ключевое слово"""
    url = 'https://www.wildberries.ru/webapi/menu/main-menu-ru-ru.json'
    response = requests.get(url)
    data = response.json()
    catalog_list = []
    for i in data:
        try:
            for child in i['childs']:
                if category in child['name']:
                    catalog_list.append({
                        'name': child['name'],
                        'url': child['url'],
                        'shard': child['shard'],
                        'query': child['query']
                    })
        except:
            continue
        try:
            for pre_child in child['childs']:
                if category in pre_child['name']:
                    catalog_list.append({
                        'name': pre_child['name'],
                        'url': pre_child['url'],
                        'shard': pre_child['shard'],
                        'query': pre_child['query']
                    })
        except:
            continue
    return catalog_list


def get_data_from_json(json_file, art):
    """Функция, ищущая нужный артикул на странице"""
    for data in json_file['data']['products']:
        if art == data['id']:
            prod = {
                'Наименование': data['name'],
                'id': data['id'],
                'Скидка': data['sale'],
                'Цена': data['priceU'],
                'Цена со скидкой': int(data["salePriceU"] / 100),
                'Бренд': data['brand'],
                'id бренда': int(data['brandId']),
                'feedbacks': data['feedbacks'],
                'rating': data['rating'],
                'Ссылка': f'https://www.wildberries.ru/catalog/{data["id"]}/detail.aspx?targetUrl=BP'
            }
            return prod
        else:
            return False


def get_content(shard, query, art):
    """функция, которая проходит по страницам нужной категории"""
    headers = {'Accept': "*/*", 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    data_list = []
    for page in range(1, 101):
        url = f'https://catalog.wb.ru/catalog/{shard}/catalog?appType=1&curr=rub&dest=-1075831,-77677,-398551,12358499' \
              f'&locale=ru&page={page}&priceU={0};{10 ** 5}' \
              f'&reg=0&regions=64,83,4,38,80,33,70,82,86,30,69,1,48,22,66,31,40&sort=popular&spp=0&{query}'
        data = requests.get(url).json()
        if get_data_from_json(data, art):
            return get_data_from_json(data, art), page
    return False


art = int(input('введите интересующий вас артикул: '))
category = input('ведите категорию данного артикула: ')
need_category = get_category(category)
for i in need_category:
    if get_content(i['shard'], i['query'], art):
        info_about_art, page = get_content(i['shard'], i['query'], art)
        print(f'нужный вам артикул найден в категории: {i["name"]} на {page} странице')
        print(info_about_art)
        break
    else:
        print(f'нужного вам артикула не нашлось в категории {i["name"]}')
