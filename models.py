class PhoneBookItem:
    """
    Класс, представляющий запись в телефонном справочнике.
    """

    def __init__(self, last_name: str, first_name: str, middle_name: str,
                 organization: str, work_phone: str, personal_phone: str):
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.organization = organization
        self.work_phone = work_phone
        self.personal_phone = personal_phone

    def __str__(self) -> str:
        """
        Возвращает строковое представление записи.
        """
        return f"{self.last_name}, {self.first_name}, {self.middle_name}, " \
               f"{self.organization}, {self.work_phone}, {self.personal_phone}"
