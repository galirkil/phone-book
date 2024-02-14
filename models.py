class PhoneBookItem:
    """Представляет объект записи телефонного справочника."""
    def __init__(self, item_id: int, last_name: str, first_name: str,
                 middle_name: str, organization: str, work_phone: str,
                 personal_phone: str):
        self.item_id = item_id
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.organization = organization
        self.work_phone = work_phone
        self.personal_phone = personal_phone
