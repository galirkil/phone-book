import json

from models import PhoneBookItem


class PhoneBookStorageJson:
    """ Отвечает за работу с базой данных."""
    def __init__(self, filename: str):
        self.filename = filename

    def load_items(self) -> list[PhoneBookItem]:
        """Загружает данные из базы данных и возращает список запсей"""
        items: list[PhoneBookItem] = []
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for notation in data:
                    item = PhoneBookItem(**notation)
                    items.append(item)
        except FileNotFoundError:
            print('Указанный файл базы данных не найден')
        return items

    def save_items(self, items: list[PhoneBookItem]) -> None:
        """Cохраняет записи в базу данных"""
        data = [item.__dict__ for item in items]
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


class PhoneBookDriver:
    """Предоставляет интерфейс для работы с записями справочника"""
    storage: PhoneBookStorageJson
    items: list[PhoneBookItem]

    def __init__(self, storage: PhoneBookStorageJson):
        self.storage = storage
        self.items = self.storage.load_items()

    def get_new_id(self) -> int:
        """Выдает ID для новой записи."""
        return len(self.items) + 1

    def add_item(self, item: PhoneBookItem) -> None:
        """Добавляет новую запись в справочник."""
        self.items.append(item)
        self.storage.save_items(self.items)

    def update_item(self, index: int, item: PhoneBookItem) -> None:
        """Заменяет данные существующей записи переданными."""
        self.items[index] = item
        self.storage.save_items(self.items)

    def search_items(self, **kwargs) -> list[PhoneBookItem]:
        """Возвращает список записей соответсвующих запросу.

        Принимает строковые значения для поиска по одному или нескольким
        полям записи.
        Возращает список записей, которые содержат запрашиваемые строки
        в соответствующих полях.
        """
        def match_search_field(item: PhoneBookItem):
            return all(
                value.lower() in getattr(item, key).lower() for
                key, value in kwargs.items()
            )
        filtered_items = filter(match_search_field, self.items)
        return list(filtered_items)

    def paginator(self, page: int, per_page: int = 10) -> list[PhoneBookItem]:
        """Возращает список записей для определенной страницы."""
        start: int = (page - 1) * per_page
        end: int = start + per_page
        return self.items[start:end]
