import uuid

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

from nex_app.enums import TransactionCommentEnum, PaymentStatusEnum

from django.db import models


class NexUser(User):
    balance = models.IntegerField(default=settings.SUBSCRIPTION_PRICE)
    inviter = models.ForeignKey("self", null=True, on_delete=models.RESTRICT)


class TokenUser(models.Model):
    user = models.ForeignKey(NexUser, on_delete=models.RESTRICT)
    token = models.CharField(max_length=64, unique=True, default=uuid.uuid4().hex)


class Server(models.Model):
    ip = models.GenericIPAddressField(protocol="IPv4", unique=True)
    private_key = models.CharField(max_length=63, unique=True)
    api_port = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(65535)]
    )
    wg_listen_port = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(65535)]
    )


class Device(models.Model):
    user = models.ForeignKey(NexUser, on_delete=models.RESTRICT)
    num = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(settings.MAX_DEVICES_ALLOWED),
        ],
    )
    active = models.BooleanField(default=True)
    end_date = models.DateField()
    private_key = models.CharField(max_length=63, unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "num"], name="unique_user_num"
            )
        ]


class IpConfig(models.Model):
    server = models.ForeignKey(
        Server, on_delete=models.RESTRICT, related_name="ip_config"
    )
    ip = models.GenericIPAddressField(protocol="IPv4")
    client = models.ForeignKey(Device, null=True, on_delete=models.SET_NULL)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["server", "ip"], name="unique_server_ip")
        ]


class PromoCode(models.Model):
    value = models.PositiveIntegerField()
    name = models.CharField(max_length=31, unique=True)
    active = models.BooleanField(default=True)
    reusable = models.BooleanField(default=False)


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    user = models.ForeignKey(NexUser, on_delete=models.RESTRICT)
    status = models.CharField(
        max_length=31,
        choices=PaymentStatusEnum.choices(),
        default=PaymentStatusEnum.PENDING,
    )


class Transaction(models.Model):
    user = models.ForeignKey(NexUser, on_delete=models.RESTRICT)
    value = models.PositiveIntegerField()
    is_credit = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=63, choices=TransactionCommentEnum.choices())
    promo_code = models.ForeignKey(PromoCode, null=True, on_delete=models.RESTRICT)
