# Generated by Django 5.1 on 2024-10-19 13:25

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("hostel", "0024_remove_maintenance_request_room"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="booking",
            name="student_id",
        ),
    ]
