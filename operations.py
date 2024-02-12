from typing import List
from models import PhoneBookItem


class PhoneBookStorageJson:
    """
    Класс, отвечающий за хранение и загрузку данных телефонного справочника.
    """

    def __init__(self, filename: str):
        self.filename = filename

    def load_items(self) -> List[PhoneBookItem]:
        """
        Загружает записи из файла и возвращает их
        в виде списка объектов PhoneBookItem.
        """
        pass

    def save_items(self, items: List[PhoneBookItem]) -> None:
        """
        Сохраняет список записей в файл.
        """
        pass


class PhoneBookOperations:
    """
    Класс, представляющий операции работы с телефонным справочником.
    """

    def __init__(self, storage: PhoneBookStorageJson):
        self.storage = storage
        self.items = self.storage.load_items()

    def add_item(self, entry: PhoneBookItem) -> None:
        """
        Добавляет новую запись в справочник.
        """
        pass

    def edit_item(self, index: int, item: PhoneBookItem) -> None:
        """
        Редактирует существующую запись в справочнике.
        """
        pass

    def search_items(self, query: str) -> List[PhoneBookItem]:
        """
        Ищет записи, содержащие заданный запрос, и возвращает их в виде списка.
        """
        pass

    def display_items(self, page: int, per_page: int = 10) -> None:
        """
        Выводит записи справочника на экран постранично.
        """
        pass
