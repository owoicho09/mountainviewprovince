# Generated by Django 5.1 on 2024-10-14 22:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hostel", "0019_hostel_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hostel",
            name="image",
            field=models.FileField(upload_to="hostel_gallery"),
        ),
    ]
