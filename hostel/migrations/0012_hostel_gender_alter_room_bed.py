# Generated by Django 5.0.6 on 2024-09-08 18:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hostel", "0011_room_bed_alter_bedspace_bed_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="hostel",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("male", "Male"), ("female", "Female")],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="room",
            name="bed",
            field=models.CharField(
                blank=True, choices=[("A,B,C", "A,B,C")], max_length=10, null=True
            ),
        ),
    ]
