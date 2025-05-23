# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField()
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True)
    first_name = models.CharField()
    last_name = models.CharField()
    email = models.CharField(unique=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class HostelHostel(models.Model):
    name = models.CharField(max_length=200)
    hid = models.CharField(primary_key=True, max_length=20)
    address = models.CharField(max_length=200)
    image = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True, null=True)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    slug = models.CharField(unique=True, max_length=50)
    date = models.DateTimeField()
    user = models.OneToOneField('StudentauthCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'hostel_hostel'


class HostelHostelfeatures(models.Model):
    icon = models.CharField(max_length=100, blank=True, null=True)
    icon_type = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField()
    hostel = models.ForeignKey(HostelHostel, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'hostel_hostelfeatures'


class HostelHostelgallery(models.Model):
    image = models.CharField(max_length=100)
    hid = models.CharField(unique=True, max_length=20)
    hostel = models.ForeignKey(HostelHostel, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'hostel_hostelgallery'


class HostelHosteltype(models.Model):
    type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    num_of_beds = models.PositiveIntegerField()
    parlour = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    atid = models.CharField(unique=True, max_length=20)
    slug = models.CharField(unique=True, max_length=50)
    date = models.DateTimeField()
    hostel = models.ForeignKey(HostelHostel, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'hostel_hosteltype'


class HostelRoom(models.Model):
    room_number = models.CharField(max_length=5000)
    is_available = models.BooleanField()
    fid = models.CharField(unique=True, max_length=20)
    date = models.DateTimeField()
    hostel = models.ForeignKey(HostelHostel, models.DO_NOTHING)
    hostel_type = models.ForeignKey(HostelHosteltype, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'hostel_room'


class StudentauthCustomuser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    fullname = models.CharField(max_length=100, blank=True, null=True)
    student_id = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=20)
    username = models.CharField(unique=True, max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'studentauth_customuser'


class StudentauthCustomuserGroups(models.Model):
    customuser = models.ForeignKey(StudentauthCustomuser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'studentauth_customuser_groups'
        unique_together = (('customuser', 'group'),)


class StudentauthCustomuserUserPermissions(models.Model):
    customuser = models.ForeignKey(StudentauthCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'studentauth_customuser_user_permissions'
        unique_together = (('customuser', 'permission'),)


class StudentauthStudentprofile(models.Model):
    pid = models.CharField(primary_key=True, max_length=15)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    postal_code = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    identity_type = models.CharField(max_length=200, blank=True, null=True)
    identity_image = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField()
    date = models.DateField()
    user = models.OneToOneField(StudentauthCustomuser, models.DO_NOTHING)
    hostel = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'studentauth_studentprofile'
