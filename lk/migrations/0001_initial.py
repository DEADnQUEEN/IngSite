# Generated by Django 4.2.16 on 2024-09-30 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('login', models.TextField(db_column='Login', unique=True)),
                ('password', models.TextField(db_column='Password')),
                ('phone', models.TextField(db_column='Phone', unique=True)),
                ('mail', models.TextField(db_column='Mail', unique=True)),
                ('last_login', models.TextField(db_column='Last Login', default=None)),
                ('is_superuser', models.IntegerField(db_column='IsRoot', default=0)),
            ],
            options={
                'verbose_name': 'Пользователь',
                'db_table': 'User',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Connect',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Connect',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('name', models.TextField(db_column='Name')),
                ('start', models.TextField(db_column='Start')),
                ('lessons', models.IntegerField(db_column='Lessons')),
            ],
            options={
                'db_table': 'Courses',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Finance',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('value', models.DecimalField(db_column='Balance', decimal_places=2, max_digits=10)),
                ('datatime', models.TextField(db_column='Datetime')),
            ],
            options={
                'db_table': 'Finance',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Human',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('name', models.TextField(db_column='Name')),
                ('surname', models.TextField(db_column='Surname')),
                ('father_name', models.TextField(db_column='Father name')),
            ],
            options={
                'db_table': 'Human',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('title', models.TextField(db_column='Title')),
                ('route', models.TextField(db_column='Route', unique=True)),
                ('template', models.TextField(db_column='Template')),
            ],
            options={
                'db_table': 'Page',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Phrase',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('phrase', models.TextField(db_column='Phrase')),
                ('tag', models.TextField(db_column='Tag')),
            ],
            options={
                'db_table': 'Phrase',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='States',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('name', models.TextField(db_column='Name')),
                ('description', models.TextField(db_column='Description')),
            ],
            options={
                'db_table': 'States',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Student',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Visits',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('student_id', models.IntegerField(db_column='Student_ID')),
                ('date', models.TextField(db_column='Date')),
                ('state_id', models.IntegerField(db_column='State_ID')),
            ],
            options={
                'db_table': 'Visits',
                'managed': False,
            },
        ),
    ]