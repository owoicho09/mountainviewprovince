# Generated by Django 5.1 on 2024-08-31 22:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("studentauth", "0004_alter_customuser_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="username",
            field=models.CharField(max_length=100),
        ),
    ]
