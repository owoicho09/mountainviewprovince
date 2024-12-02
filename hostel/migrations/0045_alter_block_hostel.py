# Generated by Django 5.1 on 2024-11-29 17:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hostel", "0044_alter_booking_flexible_plan_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="block",
            name="hostel",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="blocks",
                to="hostel.hostel",
            ),
        ),
    ]
