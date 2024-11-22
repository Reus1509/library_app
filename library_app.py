import json
import logging
import time

"""Настройки логгирования"""
logging.basicConfig(level=logging.INFO, filename='library.log', filemode='a', format='%(asctime)s - %(name)s - %('
                                                                                     'levelname)s - %(message)s')
logger = logging.getLogger(__name__)

"""Описание класса книга"""


class Book:
    def __init__(self, id, title, author, year, status):
        self._id = id
        self._title = title
        self._author = author
        self._year = year
        self._status = status

    def __dict__(self):
        return {"id": self._id, "title": self._title, "author": self._author, "year": self._year,
                "status": self._status}

    def __str__(self):
        return f'Book {self._id}: {self._title} - {self._author} - {self._year} - {self._status}'


def main_menu():
    """Функция основного меню, возращает первичный выбор пользователя"""
    logger.info("Вывожу основное меню.")
    first_choice = input(f"{'-' * 20} \n Добро пожаловать в библиотеку! \n {'-' * 20} \n Выберите пункт меню: \n "
                         f"1.Показать все "
                         "книги \n "
                         "2.Поиск "
                         "книги по "
                         "названию, автору и году \n 3.Добавить книгу \n 4.Удалить книгу по id \n 5.Изменить статус книги \n "
                         f"6.Выйти \n {'-' * 20} \n"
                         "Ваш выбор: ")
    return first_choice


def to_main_menu():
    """Функция-якорь для возвращения в основное меню"""
    second_choice = input("Введите 1 для выхода в главное меню: ")
    return second_choice


def for_search():
    """Функция получения данных от пользователя для поиска книги"""
    logger.debug('Получаю данные от пользователя для поиска книги')
    title = input('Введите название книги или нажмите Enter: ')
    author = input('Введите автора книги или нажмите Enter: ')
    year = input('Введите год книги или нажмите Enter: ')
    logger.debug('Данные получены успешно')
    return title, author, year


def for_book_add():
    """Функция получения данных от пользователя для добавления книги"""
    logger.debug('Получаю данные от пользователя для добавления книги')
    title = input('Введите название книги: ')
    author = input('Введите автора книги: ')
    year = input('Введите год издания книги: ')
    if title is None or author is None or year is None:
        logger.debug('Пользовател ввел пустое значение!')
        print("Значения не могут быть пустыми, повторите ввод!")
        for_book_add()
    logger.debug('Данные получены успешно!')
    return title, author, year


def json_to_dict_list():
    """Функция для десериализации json файла с данными о книгах в список словарей"""
    logger.debug('Начинаю сериализацию.')
    with open('library.json', 'r') as f:
        data = json.load(f)
    logger.debug('Успешно завершил считывание файла json в список словарей.')
    return data


def dict_list_to_json(library_data):
    """Функция для сериализации списка словарей в json файл"""
    logger.debug('Начинаю сериализацию списка словарей в json.')
    data = json.dumps(library_data, ensure_ascii=False)
    with open('library.json', 'w', encoding='utf-8') as f:
        f.write(data)
    logger.debug('Успешно закончил сериализацию списка словаерей в json.')


def add_book(title: str, author: str, year: str):
    """Функция для добавления книги в файл json по введенным пользователем данным"""
    try:
        logger.debug('Пробую добавить книгу пользователя!')
        library_data = json_to_dict_list()
        id = library_data[-1]['id'] + 1
        new_book = Book(id, title, author, year, 'В наличии')
        library_data.append(new_book.__dict__())
        dict_list_to_json(library_data)
    except Exception as e:
        logger.error(f'Ошибка добавления книги {e}!')


def delete_book(id: int):
    """Функция для удаления книги по id"""
    try:
        logger.debug(f"Пробую удалить книгу {id}")
        library_data = json_to_dict_list()
        for item in library_data:
            if item['id'] == int(id):
                library_data.remove(item)
        dict_list_to_json(library_data)
    except Exception as e:
        logger.error(f'Ошибка удаления книги {e}')


def search_book(title: str = None, author: str = None, year: str = None):
    """Функция поиска книги по введенным пользователем данным, можно исполльзовать комбинацию данных"""
    try:
        logger.debug(f'Начинаю поиск книги: {title}, {author}, {year}')
        library_data = json_to_dict_list()
        result_list = []
        if title:
            for item in library_data:
                if item['title'] == title:
                    result_list.append(Book(item['id'], item['title'], item['author'], item['year'], item['status']))
        if author:
            for item in library_data:
                if item['author'] == author:
                    result_list.append(Book(item['id'], item['title'], item['author'], item['year'], item['status']))
        if year:
            for item in library_data:
                if item['year'] == year:
                    result_list.append(Book(item['id'], item['title'], item['author'], item['year'], item['status']))
        if title and author and year:
            for item in library_data:
                if item['title'] == title and item['author'] == author and item['year'] == year:
                    result_list.append(Book(item['id'], item['title'], item['author'], item['year'], item['status']))
        if title and author:
            for item in library_data:
                if item['title'] == title and item['author'] == author:
                    result_list.append(Book(item['id'], item['title'], item['author'], item['year'], item['status']))
        if title and year:
            for item in library_data:
                if item['title'] == title and item['year'] == year:
                    result_list.append(Book(item['id'], item['title'], item['author'], item['year'], item['status']))
        if author and year:
            for item in library_data:
                if item['author'] == author and item['year'] == year:
                    result_list.append(Book(item['id'], item['title'], item['author'], item['year'], item['status']))
        if title is None or author is None or year is None:
            all_books()
        if not result_list:
            logger.debug('Книга не найдена по введенным данным!')
            print('Книга не найдена по заданным параметрам запроса!')
        else:
            logger.debug('Поиск книги прошел успешно!')
            for element in result_list:
                print(element.__str__())
    except Exception as e:
        logger.error(f'Ошибка поиска книги {e}!')


def all_books():
    """Функция вывода списка всех книг в библиотеке через __str__ класса Book"""
    try:
        logger.debug("Запрос на вывод списка книг")
        library_data = json_to_dict_list()
        for book in library_data:
            print(Book(book['id'], book['title'], book['author'], book['year'], book['status']))
        logger.debug("Список книг выведен успешно!")
    except Exception as e:
        logger.error(f"Ошибка вывода списка книг {e}!")


def change_status(id: int, new_status: str):
    """Функция изменения статуса книги"""
    try:
        logger.debug(f"Запрос на изменение статуса книги {id} на {new_status}")
        library_data = json_to_dict_list()
        for item in library_data:
            if item['id'] == int(id):
                item['status'] = new_status
                dict_list_to_json(library_data)
                return f'Статус книги {item["title"]} = {new_status}'
        logger.debug("Статус изменен успешно!")
    except Exception as e:
        logger.debug(f"Ошибка изменения статуса книги {e}")


def main():
    """Основная функция, содержит логику обработки введенного пользователем первичного значения."""
    while True:
        logger.info('Вывожу основное меню')
        first_choice = main_menu()

        if first_choice == '6':
            logger.info('Закрываю программу')
            break

        if first_choice == '1':
            logger.info('Вывожу перечень всех книг')
            all_books()
            second_choice = to_main_menu()
            if second_choice != '1':
                print("Вы ввели неверное значение, повторите ввод!")
                time.sleep(3)
                second_choice = to_main_menu()
            logger.info("Вывод книг успешно")

        if first_choice == '2':
            logger.info('Начинаю поиск')
            title, author, year = for_search()
            search_book(title, author, year)
            time.sleep(3)
            search_choice = input('Введите 1 чтобы повторить поиск, 2 чтобы вернуться в основное меню: ')
            while search_choice != '2':
                if search_choice == '1':
                    title, author, year = for_search()
                    search_book(title, author, year)
                    search_choice = input('Введите 1 чтобы повторить поиск, 2 чтобы вернуться в основное меню: ')
                if search_choice == '2':
                    break
                if search_choice not in (1, 3):
                    continue
                search_choice = input('Введите 1 чтобы повторить поиск, 2 чтобы вернуться в основное меню: ')
            logger.info("Поиск успешен!")

        if first_choice == '3':
            logger.info("Добавляю книгу")
            title, author, year = for_book_add()
            try:
                add_book(title, author, year)
                print('Книга добавлена успешно!')
                time.sleep(3)
            except Exception as e:
                logger.error(e)
                print("Ошибка добавления!")
                time.sleep(3)

        if first_choice == '4':
            id = input('Введите id книги, которую хотите удалить: ')
            while id == '':
                print('Вы ввели пустое значение, повторите ввод: ')
                id = input('Введите id книги, которую хотите удалить: ')
            try:
                logger.info(f'Пытаюсь удалить книгу {id}')
                delete_book(id)
                print('Книга удалена успешно!')
                logger.info(f'Книга {id} удалена успешно!')
                time.sleep(3)
            except Exception as e:
                logger.error(f'Ошибка удаления книги {e}')
                print('Ошибка удаления книги!')
                time.sleep(3)

        if first_choice == '5':
            logger.info("Пытаюсь изменить статус книги")
            id = input('Введите id книги у которой хотите изменить статус: ')
            while id == '':
                print('Вы не ввели пустое значение, повторите ввод')
                id = input('Введите id книги у которой хотите изменить статус: ')
            book_status = input('Введите 1 чтобы установить статус "Выдана" или 2 чтобы установить статус "В '
                                'наличии": ')
            if book_status not in ('1', '2'):
                while book_status not in ('1', '2'):
                    print("Вы ввели неверное значение, повторите ввод!")
                    time.sleep(3)
                    book_status = input('Введите 1 чтобы установить статус "Выдана" или 2 чтобы установить статус "В '
                                        'наличии": ')
            try:
                if book_status == '1':
                    book_status = 'Выдана'
                elif book_status == '2':
                    book_status = 'В наличии'
                logger.info(f'Пробую поменять статус книги {id} на {book_status}.')
                change_status(id, book_status)
                logger.info(f"Статус книги {id} изменен успешно!")
                print(f"Статус книги {id} изменен успешно!")
                time.sleep(3)
            except Exception as e:
                logger.error(f'Ошибка при смене статуса книги: {e}')
                print("Ошибка изменения статуса книги!")
                time.sleep(3)
        if (first_choice != '1' or first_choice != '2' or first_choice != '3' or first_choice != '4' or first_choice
                != '5' or first_choice != '6'):
            continue


if __name__ == '__main__':
    main()
