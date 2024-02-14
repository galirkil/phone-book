from operations import PhoneBookDriver, PhoneBookStorageJson
from ui import PhoneBookConsoleUI


def main() -> None:
    """Главная функция для запуска приложения."""
    storage = PhoneBookStorageJson('database/phonebook-db.json')
    driver = PhoneBookDriver(storage)
    ui = PhoneBookConsoleUI(driver, 20)
    ui.run()


if __name__ == "__main__":
    main()
