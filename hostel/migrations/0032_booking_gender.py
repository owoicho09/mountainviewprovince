# Generated by Django 5.1 on 2024-11-16 13:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hostel", "0031_hosteltype_rate_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("male", "Male"), ("female", "Female"), ("mixed", "Mixed")],
                max_length=20,
                null=True,
            ),
        ),
    ]