import hashlib
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


def model_to_dict(model: models.Model):
    fields: list[models.Field] = [*model._meta.fields]
    return {
        fields[i].name: fields[i].value_from_object(model)
        for i in range(len(fields))
    }


class Access(models.Model):
    user_id = models.AutoField(db_column='User_ID', primary_key=True)
    access = models.TextField(db_column='Access')

    def __iter__(self):
        fields: list[models.Field] = [*self._meta.fields]
        for i in range(len(fields)):
            yield fields[i].name, fields[i].value_from_object(self)

    def __str__(self):
        return str(dict(self))

    class Meta:
        managed = False
        db_table = 'Access'


class Connect(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='User_ID')
    student = models.ForeignKey('Student', models.DO_NOTHING, db_column='Student_ID')

    class Meta:
        managed = False
        db_table = 'Connect'


class Courses(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.TextField(db_column='Name')
    start = models.TextField(db_column='Start')
    lessons = models.IntegerField(db_column='Lessons')

    class Meta:
        managed = False
        db_table = 'Courses'


class Human(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.TextField(db_column='Name')
    surname = models.TextField(db_column='Surname')
    father_name = models.TextField(db_column='Father name')

    class Meta:
        managed = False
        db_table = 'Human'


class Page(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, blank=True, null=False)
    title = models.TextField(db_column='Title')
    route = models.TextField(db_column='Route', unique=True)
    template = models.TextField(db_column='Template')

    class Meta:
        managed = False
        db_table = 'Page'


class Phrase(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    phrase = models.TextField(db_column='Phrase')
    tag = models.TextField(db_column='Tag')

    class Meta:
        managed = False
        db_table = 'Phrase'


class States(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.TextField(db_column='Name')
    description = models.TextField(db_column='Description', null=False)

    class Meta:
        managed = False
        db_table = 'States'


class Student(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    human = models.ForeignKey(Human, models.DO_NOTHING, db_column='HID')
    course = models.ForeignKey(Courses, models.DO_NOTHING, db_column='Course_ID')
    state = models.ForeignKey(States, models.DO_NOTHING, db_column='State_ID')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visits = Visits.objects.filter(student_id=self.id)
        self.finance = Finance.objects.filter(student_id=self.id)

    class Meta:
        managed = False
        db_table = 'Student'


class Finance(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    student_id = models.ForeignKey(Student, models.DO_NOTHING, db_column='SID')
    value = models.DecimalField(db_column='Balance', null=False, max_digits=10, decimal_places=2)
    datatime = models.TextField(db_column='Datetime', null=False)

    class Meta:
        managed = False
        db_table = 'Finance'


class UserManager(BaseUserManager):
    def create_user(
            self,
            login: str,
            phone: str,
            name: str,
            surname: str,
            father_name: str,
            mail: str,
            password=None,
            **extra_fields
    ):
        if not mail:
            raise ValueError('The Mail field must be set')
        if not login:
            raise ValueError('The Login field must be set')
        if not phone:
            raise ValueError('The Phone field must be set')

        names = Human.objects.filter(
            name=name,
            surname=surname,
            father_name=father_name
        )

        if len(names) == 0:
            human = Human(
                name=name,
                surname=surname,
                father_name=father_name
            )
            human.save()
        else:
            human = names[0]

        mail = self.normalize_email(mail)
        user = self.model(phone=phone, mail=mail, login=login, human_id=human.id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, login, password=None, **extra_fields):
        phone = input('phone: ')
        name = input('name: ')
        surname = input('surname: ')
        father_name = input('father_name: ')
        mail = input('mail: ')
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(login, phone, name, surname, father_name, mail, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    human = models.ForeignKey(Human, models.DO_NOTHING, db_column='Human_ID')  # Field name made lowercase.
    login = models.TextField(db_column='Login', unique=True)  # Field name made lowercase.
    password = models.TextField(db_column='Password')
    phone = models.TextField(db_column='Phone', unique=True)  # Field name made lowercase.
    mail = models.TextField(db_column='Mail', unique=True)  # Field name made lowercase.
    last_login = models.TextField(db_column='Last Login', default=None)
    is_superuser = models.IntegerField(db_column='IsRoot', default=0)

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    class Meta:
        managed = False
        db_table = 'User'
        verbose_name = "Пользователь"

    def set_password(self, password: str):
        self.password = hashlib.sha3_256(password.encode()).hexdigest()


class Visits(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    student_id = models.IntegerField(db_column='Student_ID')  # Field name made lowercase.
    date = models.TextField(db_column='Date')  # Field name made lowercase.
    state_id = models.IntegerField(db_column='State_ID')  # Field name made lowercase.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        text_id = str(self.state_id)

        self.states = []
        for j in range(len(text_id) - 2, len(text_id)):
            v = States.objects.filter(id=int(text_id[j]) * (10 ** (len(text_id) - 1 - j))).first()
            if v is not None:
                self.states.append(v)

    class Meta:
        managed = False
        db_table = 'Visits'


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
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

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
