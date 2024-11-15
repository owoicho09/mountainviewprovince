# Generated by Django 5.1 on 2024-10-26 11:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hostel", "0026_alter_hostel_gender"),
    ]

    operations = [
        migrations.AddField(
            model_name="maintenance_request",
            name="description",
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name="maintenance_request",
            name="room",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="hostel.room",
            ),
        ),
    ]
