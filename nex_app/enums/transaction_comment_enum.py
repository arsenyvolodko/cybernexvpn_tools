from enum import Enum


class TransactionCommentEnum(Enum):
    RENEW_SUBSCRIPTION = "Продление подписки"
    INVITATION = "Приглашение пользователя"
    START_BALANCE = "Стартовый баланс"
    FILL_UP_BALANCE = "Пополнение баланса"
    ADD_DEVICE = "Добавление устройства"
    PROMO_CODE = "Применение промокода"
    EDIT_BY_ADMIN = "Изменено админом"

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]
