# Generated by Django 5.0.6 on 2024-09-16 13:48

import django.db.models.deletion
import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hostel", "0016_hosteltype_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="HostelTypeGallery",
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
                ("image", models.ImageField(upload_to="hostel_type_gallery")),
                (
                    "hid",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                        length=10,
                        max_length=20,
                        prefix="",
                        unique=True,
                    ),
                ),
                (
                    "hostel_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hostel.hosteltype",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Hostel Type Gallery",
            },
        ),
    ]
