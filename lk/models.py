import hashlib
import django.contrib.auth.models
from django.db import models
import datetime


def model_to_dict(model: models.Model):
    fields: list[models.Field] = [*model._meta.fields]
    return {
        fields[i].name: fields[i].value_from_object(model)
        for i in range(len(fields))
    }


def get_states_by_id(state_id: int):
    text_id = str(state_id)

    states = []
    for j in range(2):
        if j < len(text_id):
            v = States.objects.filter(id=int(text_id[len(text_id) - 1 - j]) * (10 ** j)).first()
            if v is not None:
                states.append(v)

    return states


class Connect(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='User_ID')
    student_id = models.ForeignKey('Student', models.DO_NOTHING, db_column='Student_ID')

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


class States(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.TextField(db_column='Name')
    description = models.TextField(db_column='Description', null=False)

    class Meta:
        managed = False
        db_table = 'States'


class Student(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    human_id = models.ForeignKey(Human, models.DO_NOTHING, db_column='HID')
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


class UserManager(django.contrib.auth.models.BaseUserManager):
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
            human_id = Human(
                name=name,
                surname=surname,
                father_name=father_name
            )
            human_id.save()
        else:
            human_id = names[0]

        mail = self.normalize_email(mail)
        user = self.model(phone=phone, mail=mail, login=login, human_id=human_id.id, **extra_fields)
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


class User(django.contrib.auth.models.AbstractBaseUser, django.contrib.auth.models.PermissionsMixin):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    human_id = models.ForeignKey(Human, models.DO_NOTHING, db_column='Human_ID')  # Field name made lowercase.
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
        self.dt = datetime.datetime.strptime(self.date, '%Y-%m-%d %H:%M')

    @property
    def year(self):
        return self.dt.strftime('%Y')

    @property
    def month(self):
        return self.dt.strftime('%m')

    @property
    def day(self):
        return self.dt.strftime('%d')

    @property
    def hour(self):
        return self.dt.strftime('%H')

    @property
    def minute(self):
        return self.dt.strftime('%M')

    @property
    def states(self) -> list[States]:
        return get_states_by_id(self.state_id)

    class Meta:
        managed = False
        db_table = 'Visits'
