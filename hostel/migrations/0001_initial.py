# Generated by Django 5.1 on 2024-12-02 16:22

import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BedSpace",
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
                    "bed_type",
                    models.CharField(choices=[("A,B,C", "A,B,C")], max_length=20),
                ),
                ("is_booked", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="ReminderDays",
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
                    "days",
                    models.PositiveIntegerField(
                        default=30,
                        help_text="Number of days before sending reminder emails",
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Review",
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
                ("fullname", models.CharField(max_length=100)),
                ("review", models.TextField(blank=True, null=True)),
                ("reply", models.CharField(blank=True, max_length=1000, null=True)),
                (
                    "rating",
                    models.IntegerField(
                        choices=[
                            (1, "★☆☆☆☆"),
                            (2, "★★☆☆☆"),
                            (3, "★★★☆☆"),
                            (4, "★★★★☆"),
                            (5, "★★★★★"),
                        ],
                        default=None,
                    ),
                ),
                ("active", models.BooleanField(default=False)),
                ("date", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "Reviews & Rating",
                "ordering": ["-date"],
            },
        ),
        migrations.CreateModel(
            name="Room",
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
                ("room_number", models.CharField(max_length=5000)),
                (
                    "bed",
                    models.CharField(
                        blank=True,
                        choices=[("A,B,C", "A,B,C")],
                        max_length=10,
                        null=True,
                    ),
                ),
                ("capacity", models.PositiveIntegerField(blank=True, null=True)),
                ("current_occupancy", models.PositiveIntegerField(default=0)),
                (
                    "avilable_bedspace",
                    models.PositiveIntegerField(blank=True, default=0, null=True),
                ),
                ("is_available", models.BooleanField(default=True)),
                (
                    "fid",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                        length=10,
                        max_length=20,
                        prefix="",
                        unique=True,
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "Room",
            },
        ),
        migrations.CreateModel(
            name="Hostel",
            fields=[
                ("name", models.CharField(max_length=200)),
                (
                    "hid",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                        length=7,
                        max_length=20,
                        prefix="",
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("address", models.CharField(max_length=200)),
                ("image", models.FileField(upload_to="hostel_gallery")),
                (
                    "description",
                    models.CharField(blank=True, max_length=1000, null=True),
                ),
                ("phone", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=200)),
                ("active", models.BooleanField(blank=True, default=True, null=True)),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("male", "Male"),
                            ("female", "Female"),
                            ("mixed", "Mixed"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "rating",
                    models.CharField(
                        blank=True,
                        choices=[
                            (1, "★☆☆☆☆"),
                            (2, "★★☆☆☆"),
                            (3, "★★★☆☆"),
                            (4, "★★★★☆"),
                            (5, "★★★★★"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                ("slug", models.SlugField(unique=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hostels",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "hostel_hostel",
            },
        ),
        migrations.CreateModel(
            name="Block",
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
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="hostel_gallery"
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("male", "Male"),
                            ("female", "Female"),
                            ("mixed", "Mixed"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "bid",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                        length=10,
                        max_length=20,
                        prefix="",
                        unique=True,
                    ),
                ),
                ("slug", models.SlugField(unique=True)),
                (
                    "hostel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="blocks",
                        to="hostel.hostel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HostelGallery",
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
                ("image", models.ImageField(upload_to="hostel_gallery")),
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
                    "hostel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="hostel.hostel"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Hostel Gallery",
            },
        ),
        migrations.CreateModel(
            name="HostelType",
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
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="hostel_gallery"
                    ),
                ),
                ("type", models.CharField(max_length=100)),
                (
                    "rate_type",
                    models.CharField(
                        blank=True,
                        choices=[("semester", "Semester"), ("session", "Session")],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "baze_price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
                ),
                (
                    "semester_rate",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "session_rate",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("num_of_beds", models.PositiveIntegerField(default=1)),
                ("parlour", models.PositiveIntegerField(default=0)),
                ("capacity", models.PositiveIntegerField(default=2)),
                (
                    "atid",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                        length=10,
                        max_length=20,
                        prefix="",
                        unique=True,
                    ),
                ),
                ("slug", models.SlugField(unique=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "block",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hostel_types",
                        to="hostel.block",
                    ),
                ),
                (
                    "hostel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="hostel.hostel"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Hostel Type",
            },
        ),
        migrations.CreateModel(
            name="HostelFeatures",
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
                ("icon", models.CharField(blank=True, max_length=100, null=True)),
                ("icon_type", models.CharField(blank=True, max_length=100, null=True)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "hostel_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hostel.hosteltype",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Hostel Features",
            },
        ),
        migrations.CreateModel(
            name="Booking",
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
                ("fullname", models.CharField(blank=True, max_length=100, null=True)),
                ("email", models.EmailField(blank=True, max_length=100, null=True)),
                ("phone", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "school",
                    models.CharField(
                        blank=True,
                        choices=[("nile", "Nile"), ("baze", "Baze")],
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("male", "Male"),
                            ("female", "Female"),
                            ("mixed", "Mixed"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "rate_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("semester", "Semester"),
                            ("session", "Session"),
                            ("flexible plan", "Flexible Plan"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "rate_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "flexible_plan_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("semester", "Semester"),
                            ("session", "Session"),
                            ("flexible plan", "Flexible Plan"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "initial_payment",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "remaining_balance",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0.0,
                        max_digits=10,
                        null=True,
                    ),
                ),
                ("payment_due_date", models.DateField(blank=True, null=True)),
                (
                    "reminder_sent",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "check_in_tracker",
                    models.BooleanField(
                        default=False,
                        help_text="CHECK THIS BOX ONLY WHEN STUDENT CHECKS IN",
                    ),
                ),
                (
                    "check_out_tracker",
                    models.BooleanField(
                        default=False,
                        help_text="CHECK THIS BOX ONLY WHEN STUDENT CHECKS OUT",
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "stripe_payment",
                    models.CharField(blank=True, max_length=1000, null=True),
                ),
                (
                    "payment_status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Processing", "Processing"),
                            ("Paid", "Paid"),
                            ("Declined", "Declined"),
                            ("In-review", "In-review"),
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "success_id",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                        length=10,
                        max_length=505,
                        prefix="",
                    ),
                ),
                (
                    "booking_id",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                        length=10,
                        max_length=20,
                        prefix="",
                        unique=True,
                    ),
                ),
                (
                    "block",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hostel.block",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "hostel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="hostel.hostel"
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
        ),
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
        migrations.CreateModel(
            name="Maintenance_request",
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
                ("request", models.CharField(blank=True, max_length=1000, null=True)),
                (
                    "issue_category",
                    models.CharField(
                        choices=[
                            ("electrical issue", "Electrical Issue"),
                            ("plumbing", "Plumbing"),
                            ("appliances", "Appliances"),
                            ("lock/key issue", "Lock/Key Issue"),
                            ("others", "Others"),
                        ],
                        max_length=200,
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, max_length=5000, null=True),
                ),
                ("active", models.BooleanField(default=False)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "booking",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="hostel.booking",
                    ),
                ),
                (
                    "helpful",
                    models.ManyToManyField(
                        blank=True, related_name="helpful", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "hostel",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="hostel.hostel",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Maintenance Request",
                "ordering": ["-date"],
            },
        ),
        migrations.CreateModel(
            name="Notification",
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
                    "type",
                    models.CharField(
                        choices=[
                            ("Booking Confirmed", "Booking Confirmed"),
                            ("Booking Cancelled", "Booking Cancelled"),
                        ],
                        max_length=100,
                    ),
                ),
                ("seen", models.BooleanField(default=False)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "booking",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="hostel.booking",
                    ),
                ),
            ],
        ),
    ]
