import math
from typing import Callable, ValuesView

from tabulate import tabulate

from models import PhoneBookItem
from operations import PhoneBookDriver


class PhoneBookConsoleUI:
    """Отвечает за пользовательский интерфейс."""
    driver: PhoneBookDriver
    items_per_page: int
    columns: list[str]
    menu_commands: dict[str, Callable]

    def __init__(self, driver: PhoneBookDriver, per_page: int = 10):
        self.driver = driver
        self.items_per_page = per_page
        self.columns = [
            "ID", "Фамилия", "Имя", "Отчество",
            "Название организации", "Телефон рабочий",
            "Телефон личный"
        ]
        self.menu_commands = {
            '1': self.show_items_paginated,
            '2': self.add_item,
            '3': self.edit_item,
            '4': self.find_items,
            '5': exit
        }

    @staticmethod
    def print_menu() -> None:
        """Выводит основное меню в терминал"""
        print('Вам доступны следующии компанды:')
        print("1. Показать существующие записи.")
        print("2. Добавить новую запись.")
        print("3. Редактировать существующую запись.")
        print("4. Искать записи.")
        print("5. Завершить работу.")

    def show_items_paginated(self) -> None:
        """Выводит записи в терминал постранично."""
        page: int = 1
        max_pages: int = math.ceil(
            len(self.driver.items) / self.items_per_page
        )

        def render_page() -> None:
            """Выводит страницу на печать."""
            nonlocal page
            print(f'Страница {page} из {max_pages}:')
            items_to_show = self.driver.paginator(page, self.items_per_page)
            rows: list[ValuesView] = [vars(item).values() for item
                                      in items_to_show]
            print(tabulate(rows, headers=self.columns, tablefmt='pretty'))

        def go_to_next_page() -> None:
            """Выводит на печать следующую страницу списка записей."""
            nonlocal page, max_pages
            if page == max_pages:
                print('Это последняя страница')
                return
            page += 1
            print('Переход на следующую страницу...')
            render_page()

        def go_to_previous_page() -> None:
            """Выводит на печать предыдущую страницу списка записей."""
            nonlocal page
            if page == 1:
                print('Вы уже находитесь на самой первой странице')
                return
            page -= 1
            print('Переход на предыдущую страницу...')
            render_page()

        print('Показать существующие записи...')
        render_page()
        while True:
            choice = input(
                "Введите 'n' для следующей страницы, "
                "'p' для предыдущей страницы, 'q' для выхода в главное меню: "
            )
            if choice == 'n':
                go_to_next_page()
            elif choice == 'p':
                go_to_previous_page()
            elif choice == 'q':
                print('Возврат в главное меню...')
                return
            else:
                print(
                    "Некорректная команда. "
                    "Пожалуйста, выберите 'n', 'p' или 'q'."
                )

    def add_item(self) -> None:
        print('Добавление новой записи...')
        item_data = {
            'item_id': self.driver.get_new_id(),
            'last_name': input("Введите фамилию: "),
            'first_name': input("Введите имя: "),
            'middle_name': input("Введите отчество: "),
            'organization': input("Введите название организации: "),
            'work_phone': input("Введите рабочий телефон: "),
            'personal_phone': input("Введите личный телефон: ")
        }
        item = PhoneBookItem(**item_data)
        self.driver.add_item(item)
        print('Новая запись успешно добавлена!')

    def edit_item(self) -> None:
        print('Редактирование существующей записи...')
        max_item_id = len(self.driver.items)
        while True:
            try:
                item_id = int(
                    (input('Введите ID записи для редактирования: '))
                )
                if not 0 < item_id <= max_item_id:
                    raise ValueError
                break
            except ValueError:
                print(
                    f'Некорректный ввод! '
                    f'Введите числовое значение от 1 до {max_item_id}'
                )
        item_to_edit: PhoneBookItem = self.driver.items[item_id - 1]
        print(
            "Введите новые значения "
            "(оставьте поле пустым, чтобы сохранить текущее значение):"
        )

        last_name = input(
            f"Фамилия (текущая: {item_to_edit.last_name}): "
        ) or item_to_edit.last_name

        first_name = input(
            f"Имя (текущее: {item_to_edit.first_name}): "
        ) or item_to_edit.first_name

        middle_name = input(
            f"Отчество (текущее: {item_to_edit.middle_name}): "
        ) or item_to_edit.middle_name

        organization = input(
            f"Организация (текущая: {item_to_edit.organization}): "
        ) or item_to_edit.organization

        work_phone = input(
            f"Рабочий телефон (текущий: {item_to_edit.work_phone}): "
        ) or item_to_edit.work_phone

        personal_phone = input(
            f"Личный телефон (текущий: {item_to_edit.personal_phone}): "
        ) or item_to_edit.personal_phone

        new_item = PhoneBookItem(item_id, last_name, first_name, middle_name,
                                 organization, work_phone, personal_phone)
        self.driver.update_item(item_id - 1, new_item)
        print('Запись успешно отредактирована!')

    def find_items(self) -> None:
        print('Поиск записей...')
        search_fields: dict[str, str] = {}
        print(
            "Введите значения для поиска "
            "(оставьте поле пустым, если не хотите использовать):"
        )

        last_name = input("Фамилия: ")
        if last_name:
            search_fields['last_name'] = last_name

        first_name = input("Имя: ")
        if first_name:
            search_fields['first_name'] = first_name

        middle_name = input("Отчество: ")
        if middle_name:
            search_fields['middle_name'] = middle_name

        organization = input("Название организации: ")
        if organization:
            search_fields['organization'] = organization

        work_phone = input("Рабочий телефон: ")
        if work_phone:
            search_fields['work_phone'] = work_phone

        personal_phone = input("Личный телефон: ")
        if personal_phone:
            search_fields['personal_phone'] = personal_phone

        found_items: list[PhoneBookItem] = self.driver.search_items(
            **search_fields)
        item_fields: list[ValuesView] = [vars(found_item).values() for
                                         found_item in found_items]
        print('По вашему запросу найдены следующие записи:')
        print(tabulate(item_fields, headers=self.columns, tablefmt='pretty'))

    def run(self) -> None:
        print('Добро пожаловать в телефонный справочник!')
        while True:
            PhoneBookConsoleUI.print_menu()
            choice: str = input("Введите номер команды: ")
            command: Callable = self.menu_commands.get(choice)
            if command:
                command()
            else:
                print(
                    'Некорректный ввод. Пожалуйста выберите команду из списка')
