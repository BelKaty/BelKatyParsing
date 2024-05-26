# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BookparserPipeline:
    """
    Класс Pipeline (Трубопровод), настраиваем БД, чистим данные и записываем их БД

     Методы:
    -  process_item(self, item, spider): Функция 'чистит' данные и записывает их в БД MongoDB.

     Dunder методы:
    - __init__(self): конструктор класса.
    """

    def __init__(self):
        # Настраиваем клиент MongoDB (IP, порт)
        client = MongoClient('localhost', 27017)
        # Задаём название базы данных ('books')
        self.mongo_base = client.books
        # Счетчик обработанных страниц
        self.count_page = 0

    def process_item(self, item, spider):
        """
        Функция 'чистит' данные и записывает их в БД MongoDB

        :param item: данные пришедшие из парсера
        :param spider:
        :return: очищенные данные, запись в БД
        """
        # Создаём коллекцию в БД (имя нашего паука)
        collection = self.mongo_base[spider.name]

        # Задание id
        try:
            *_, id, _ = item['link'].split('/')
            item['_id'] = id
        except ValueError:
            item['_id'] = None

        # Обработка названия книги
        _, name = item.get('name').split(':')
        item['name'] = name.strip()

        # Обработка авторов книги
        item['author'] = ', '.join(item['author'])

        # Обработка переводчиков книги
        item['translator'] = ', '.join(item['translator'])

        # Обработка художников книги
        item['artist'] = ', '.join(item['artist'])

        # Обработка рецензентов
        item['editor'] = ', '.join(item['editor'])

        # Обработка издательств
        item['publishing'] = ', '.join(item['publishing'])

        # Обработка года издания книги
        try:
            *_, year, _ = item['year'][1].split(' ')
            item['year'] = int(year)
        except ValueError:
            item['year'] = None

        # Обработка серии
        item['series'] = ', '.join(item['series'])

        # Обработка коллекции
        item['collection'] = ', '.join(item['collection'])

        # Обработка жанра книги
        item['genre'] = ', '.join(item['genre'])

        # Обработка массы книги
        try:
            *_, weight, _ = item['weight'].split(' ')
            item['weight'] = int(weight)
        except ValueError:
            item['weight'] = None

        # Обработка размеров книги
        try:
            *_, dimensions, _ = item['dimensions'].split(' ')
            length, width, height = dimensions.split('x')
            item['dimensions'] = {'length': int(length), 'width': int(width), 'height': int(height)}
        except ValueError:
            item['dimensions'] = {'length': None, 'width': None, 'height': None}

        # Обработка рейтинга книги
        try:
            item['rating'] = float(item['rating'])
        except ValueError:
            item['rating'] = None

        # Обработка цены книги
        try:
            item['price'] = float(item['price'])
        except ValueError:
            item['price'] = None

        try:
            # Добавляем запись в базу данных
            collection.insert_one(item)
        except ValueError:
            print('Ошибка добавления документа')

        # Выводим информацию о состоянии процесса
        self.count_page += 1
        print(f'Обработано {self.count_page} книг')

        return item
