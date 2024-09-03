from enum import Enum


class PaymentStatusEnum(Enum):
    PENDING = "Ожидает оплаты"
    CANCELED = "Отменен"
    SUCCEEDED = "Успешно оплачен"

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]
