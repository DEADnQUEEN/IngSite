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


class States(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(db_column='Name', null=False, max_length=20, verbose_name="Название статуса")
    description = models.TextField(db_column='Description', null=False, default='?', verbose_name="Описание статуса")

    class Meta:
        managed = True
        db_table = 'States'
        verbose_name = "Статус"

    def __str__(self):
        return f"{self.id}: {self.name}"


class Courses(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(
        db_column='Name', max_length=20, verbose_name="Название курса", blank=False, null=False
    )
    date = models.DateField(
        db_column='Date', verbose_name="Дата", blank=False, null=False
    )
    time = models.TimeField(
        db_column='Time', verbose_name="Время", blank=False, null=False
    )
    lessons = models.IntegerField(
        db_column='Lessons', verbose_name="Количество занятий", blank=False, null=False
    )

    class Meta:
        managed = True
        db_table = 'Courses'
        verbose_name = "Курс"

    def __str__(self):
        return f"{self._meta.verbose_name}: {self.name}"


class Human(models.Model):
    id = models.AutoField(
        db_column='ID', primary_key=True
    )
    name = models.CharField(
        db_column='Name', null=False, max_length=20, verbose_name="Имя", blank=False
    )
    surname = models.CharField(
        db_column='Surname', null=False, max_length=20, verbose_name="Фамилия", blank=False
    )
    father_name = models.CharField(
        db_column='Father name', null=True, blank=True, max_length=20, verbose_name="Отчество"
    )

    class Meta:
        managed = True
        db_table = 'Human'
        verbose_name = "Имя"

    @property
    def full_name(self):
        full_name = [self.surname, self.name]
        if self.father_name is not None:
            full_name.append(self.father_name)
        return ' '.join(full_name)

    def __str__(self):
        return self.full_name


class UserManager(django.contrib.auth.models.BaseUserManager):
    def create_user(
            self,
            login: str,
            name: str,
            surname: str,
            father_name: str,
            password=None,
            **extra_fields
    ):
        if not login:
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

        user = self.model(login=login, human=human, human_id=human.id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, login, password=None, **extra_fields):
        name = input('name: ')
        surname = input('surname: ')
        father_name = input('father_name: ')
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(login, name, surname, father_name, password, **extra_fields)


class User(django.contrib.auth.models.AbstractBaseUser, django.contrib.auth.models.PermissionsMixin):
    id = models.AutoField(
        db_column='ID', primary_key=True, null=False, verbose_name="ID"
    )
    human = models.ForeignKey(
        Human, models.DO_NOTHING, null=False, verbose_name="Имя человека", blank=False
    )
    login = models.CharField(
        db_column='Login', unique=True, verbose_name="Телефон", max_length=11, null=False, blank=False
    )
    password = models.CharField(
        db_column='Password', max_length=20, null=False, verbose_name="Пароль", blank=False
    )
    last_login = models.TextField(
        db_column='Last Login', default=None, null=True, blank=True
    )
    is_superuser = models.IntegerField(
        db_column='IsRoot', default=0, verbose_name="Суперпользователь", blank=False, null=False
    )

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    class Meta:
        managed = True
        db_table = 'User'
        verbose_name = "Пользователь"

    def set_password(self, password: str):
        self.password = hashlib.sha3_256(password.encode()).hexdigest()

    def __str__(self):
        return f'{self.login}: {self.human}'


class Student(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    human = models.ForeignKey(
        Human,
        models.DO_NOTHING,
        verbose_name="Имя",
        blank=False,
        null=False
    )
    course = models.ForeignKey(
        Courses, models.DO_NOTHING,
        verbose_name="Курс",
        default=Courses.objects.get(id=1),
        blank=False,
        null=False
    )
    state = models.ForeignKey(
        States,
        models.DO_NOTHING,
        verbose_name="Статус",
        default=States.objects.get(id=1),
        blank=False,
        null=False
    )

    @property
    def visits(self):
        return Visits.objects.filter(student_id=self.id)

    @property
    def finance(self):
        return Finance.objects.filter(student_id=self.id)

    @property
    def coins(self):
        return Coins.objects.filter(student_id=self.id)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'Student'
        verbose_name = "Студент"

    def __str__(self):
        return f"{self._meta.verbose_name} {self.id}: {self.human}"

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
    id = models.AutoField(db_column='ID', primary_key=True, verbose_name="ID")
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING, db_column='Student_ID', verbose_name="Студент")
    amount = models.DecimalField(db_column='Balance', null=False, default=0, max_digits=10, decimal_places=2, verbose_name="Количество")
    data = models.DateField(db_column='Date', null=False, verbose_name="Дата")
    time = models.TimeField(db_column="Time", null=False, verbose_name="Время")

    class Meta:
        managed = True
        db_table = 'Finance'
        verbose_name = "Финансы"

    def __str__(self):
        return f"Оплата {self.id} -> {self.student}"


class Coins(models.Model):
    id = models.AutoField(
        db_column='ID',
        primary_key=True,
        blank=False,
        null=False
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.DO_NOTHING,
        db_column='Student_ID',
        verbose_name="Студент",
        blank=False,
        null=False
    )
    amount = models.DecimalField(
        db_column='Balance',
        null=False,
        max_digits=10,
        decimal_places=2,
        verbose_name="Количество",
        blank=False,
        default=0,
    )
    data = models.DateField(
        db_column='Date',
        null=False,
        verbose_name="Дата",
        blank=False,
    )

    class Meta:
        managed = True
        db_table = 'Coins'
        verbose_name = 'Совокоины'

    def __str__(self):
        return str(self.student)


class Visits(models.Model):
    id = models.AutoField(
        db_column='ID',
        primary_key=True,
        blank=False,
        null=False
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.DO_NOTHING,
        db_column='Student_ID',
        verbose_name='Студент',
        blank=False,
        null=False
    )
    date = models.DateField(
        db_column='Date',
        null=False,
        verbose_name="Дата",
        blank=False,
    )
    time = models.TimeField(
        db_column='Time',
        null=False,
        verbose_name="Время",
        blank=False,
    )
    state_id = models.IntegerField(
        db_column='State_ID',
        null=False,
        verbose_name="Статус",
        default=1,
        blank=False,
    )

    class Meta:
        managed = True
        db_table = 'Visits'
        verbose_name = "Посещения"

    def __str__(self):
        return f"{self.id}: {self.student.__str__()}"


class Connect(models.Model):
    id = models.AutoField(
        db_column='ID',
        primary_key=True,
        blank=False,
        null=False
    )
    user = models.ForeignKey(
        User,
        models.DO_NOTHING,
        verbose_name="Пользователь",
        blank=False,
        null=False
    )
    student = models.ForeignKey(
        Student,
        models.DO_NOTHING,
        verbose_name="Студент",
        blank=False,
        null=False
    )

    class Meta:
        managed = True
        db_table = 'Connect'
        verbose_name = "Соединение"

    def __str__(self):
        return f"{self.user} -> {self.student}"
