import logging


class PhoneNumberFilter(logging.Filter):
    def __init__(self, name: str = "", display_digits: int = 4) -> None:
        super().__init__(name)
        self.display_digits = display_digits

    def filter(self, record: logging.LogRecord) -> bool:
        if "phone" in record.__dict__:
            phone_length = len(record.phone)  # type: ignore
            to_hide = "*" * (phone_length - self.display_digits)
            to_dispaly = record.phone[-(self.display_digits):]  # type: ignore
            record.phone = to_hide + to_dispaly
        return super().filter(record)
