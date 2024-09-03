# Generated by Django 5.1.1 on 2024-09-03 20:16

import django.contrib.auth.models
import django.core.validators
import django.db.models.deletion
import nex_app.enums.payment_status_enum
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="PromoCode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.PositiveIntegerField()),
                ("name", models.CharField(max_length=31, unique=True)),
                ("active", models.BooleanField(default=True)),
                ("reusable", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Server",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ip", models.GenericIPAddressField(protocol="IPv4", unique=True)),
                ("private_key", models.CharField(max_length=63, unique=True)),
                (
                    "api_port",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(65535),
                        ]
                    ),
                ),
                (
                    "wg_listen_port",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(65535),
                        ]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NexUser",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("balance", models.IntegerField(default=100)),
                (
                    "inviter",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="nex_app.nexuser",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("auth.user",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "device_num",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(3),
                        ]
                    ),
                ),
                ("active", models.BooleanField(default=True)),
                ("end_date", models.DateField()),
                ("private_key", models.CharField(max_length=63, unique=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="nex_app.nexuser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.UUIDField(editable=False, primary_key=True, serialize=False),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Ожидает оплаты"),
                            ("CANCELED", "Отменен"),
                            ("SUCCEEDED", "Успешно оплачен"),
                        ],
                        default=nex_app.enums.payment_status_enum.PaymentStatusEnum[
                            "PENDING"
                        ],
                        max_length=31,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="nex_app.nexuser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="IpConfig",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ip", models.GenericIPAddressField(protocol="IPv4")),
                (
                    "client",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="nex_app.client",
                    ),
                ),
                (
                    "server",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="ip_config",
                        to="nex_app.server",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TokenUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "token",
                    models.CharField(
                        default="fe755868afb24b18b416dce2624ed75b",
                        max_length=64,
                        unique=True,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="nex_app.nexuser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.PositiveIntegerField()),
                ("is_credit", models.BooleanField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "comment",
                    models.CharField(
                        choices=[
                            ("RENEW_SUBSCRIPTION", "Продление подписки"),
                            ("INVITATION", "Приглашение пользователя"),
                            ("START_BALANCE", "Стартовый баланс"),
                            ("FILL_UP_BALANCE", "Пополнение баланса"),
                            ("ADD_DEVICE", "Добавление устройства"),
                            ("PROMO_CODE", "Применение промокода"),
                            ("EDIT_BY_ADMIN", "Изменено админом"),
                        ],
                        max_length=63,
                    ),
                ),
                (
                    "promo_code",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="nex_app.promocode",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="nex_app.nexuser",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="client",
            constraint=models.UniqueConstraint(
                fields=("user", "device_num"), name="unique_user_device_num"
            ),
        ),
        migrations.AddConstraint(
            model_name="ipconfig",
            constraint=models.UniqueConstraint(
                fields=("server", "ip"), name="unique_server_ip"
            ),
        ),
    ]
