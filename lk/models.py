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


def get_states_by_id(state_id: int) -> list:
    text_id = str(state_id)

    states = []
    for j in range(len(text_id)):
        v = States.objects.filter(id=int(text_id[len(text_id) - 1 - j]) * (10 ** j)).first()
        if v is not None:
            states.append(v)

    return states


class Connect(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    student = models.ForeignKey('Student', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'Connect'


class Courses(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.TextField(db_column='Name')
    date = models.DateField(db_column='Date')
    time = models.TimeField(db_column='Time')
    lessons = models.IntegerField(db_column='Lessons')

    class Meta:
        managed = True
        db_table = 'Courses'


class Human(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.TextField(db_column='Name', null=False)
    surname = models.TextField(db_column='Surname', null=False)
    father_name = models.TextField(db_column='Father name')

    class Meta:
        managed = True
        db_table = 'Human'


class States(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.TextField(db_column='Name', null=False)
    description = models.TextField(db_column='Description', null=False, default='?')

    class Meta:
        managed = True
        db_table = 'States'


class Student(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    human = models.ForeignKey(Human, models.DO_NOTHING)
    course = models.ForeignKey(Courses, models.DO_NOTHING)
    state = models.ForeignKey(States, models.DO_NOTHING)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visits = Visits.objects.filter(student_id=self.id)
        self.finance = Finance.objects.filter(student_id=self.id)

    class Meta:
        managed = True
        db_table = 'Student'

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)
        date = self.course.date
        for i in range(self.course.lessons):
            date += datetime.timedelta(days=7)
            v = Visits.objects.create(
                student=self,
                state_id=10,
                date=date,
                time=self.course.time
            )
            v.save()


class Finance(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    student = models.ForeignKey(Student, models.DO_NOTHING, default=0)
    value = models.DecimalField(db_column='Balance', null=False, max_digits=10, decimal_places=2)
    data = models.DateField(db_column='Date', null=False)
    time = models.TimeField(db_column="Time", null=False)

    class Meta:
        managed = True
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

        human = Human.objects.filter(
            name=name,
            surname=surname,
            father_name=father_name
        ).first()

        if human is None:
            human = Human(
                name=name,
                surname=surname,
                father_name=father_name
            )
            human.save()

        mail = self.normalize_email(mail)
        user = self.model(phone=phone, mail=mail, login=login, human=human, human_id=human.id, **extra_fields)
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
    id = models.AutoField(db_column='ID', primary_key=True)
    human = models.ForeignKey(Human, models.DO_NOTHING)
    login = models.TextField(db_column='Login', unique=True)
    password = models.TextField(db_column='Password')
    phone = models.TextField(db_column='Phone', unique=True)
    mail = models.TextField(db_column='Mail', unique=True)
    last_login = models.TextField(db_column='Last Login', default=None, null=True, blank=True)
    is_superuser = models.IntegerField(db_column='IsRoot', default=0)

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'User'
        verbose_name = "Пользователь"

    def set_password(self, password: str):
        self.password = hashlib.sha3_256(password.encode()).hexdigest()


class Visits(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING, db_column='Student_ID')
    date = models.DateField(db_column='Date', null=False)
    time = models.TimeField(db_column='Time', null=False)
    state_id = models.IntegerField(db_column='State_ID', null=False)

    @property
    def states(self) -> list[States]:
        return get_states_by_id(self.state_id)

    class Meta:
        managed = True
        db_table = 'Visits'
