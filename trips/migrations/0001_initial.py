# Generated by Django 3.0 on 2019-12-20 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('phone_number', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Номер телефона')),
                ('reg_date', models.DateField(verbose_name='Дата регистрации')),
                ('passport_num', models.PositiveIntegerField(verbose_name='Номер паспорта')),
                ('passport_ser', models.PositiveIntegerField(verbose_name='Серия паспорта')),
                ('surname', models.CharField(max_length=20, verbose_name='Фамилия')),
                ('name', models.CharField(max_length=20, verbose_name='Имя')),
                ('mid_name', models.CharField(max_length=20, verbose_name='Отчество')),
                ('issued_by', models.TextField(verbose_name='Кем выдан паспорт')),
                ('issued_date', models.DateField(verbose_name='Дата выдачи пасспорта')),
                ('birth_date', models.DateField(verbose_name='Дата рождения')),
                ('citizenship', models.CharField(max_length=50, verbose_name='Гражданство')),
                ('region', models.CharField(blank=True, max_length=50, verbose_name='Регион')),
                ('city', models.CharField(max_length=20, verbose_name='Город')),
                ('street', models.CharField(max_length=100, verbose_name='Улица')),
                ('house', models.PositiveSmallIntegerField(verbose_name='Дом')),
                ('corpus', models.CharField(blank=True, max_length=2, verbose_name='Корпус')),
                ('flat', models.PositiveSmallIntegerField(verbose_name='Квартира')),
                ('zip_code', models.PositiveIntegerField(verbose_name='Индекс')),
                ('notes', models.TextField(blank=True, verbose_name='Замечания')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Название')),
                ('visa_required', models.BooleanField(verbose_name='Обязательность визы')),
                ('passport_required', models.BooleanField(verbose_name='Обязательность загранпаспорта')),
                ('visa_price', models.PositiveIntegerField(blank=True, null=True, verbose_name='Цена визы')),
                ('passport_price', models.PositiveIntegerField(blank=True, null=True, verbose_name='Цена загранпаспорта')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('number', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Название маршрута')),
                ('description', models.TextField(verbose_name='Описание маршрута')),
                ('price', models.PositiveIntegerField(verbose_name='Цена')),
                ('duration', models.PositiveIntegerField(verbose_name='Длительность')),
            ],
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='Тип транспорта')),
            ],
        ),
        migrations.CreateModel(
            name='Visa',
            fields=[
                ('number', models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='Номер визы')),
                ('country', models.CharField(max_length=20, verbose_name='Страна')),
                ('issued_date', models.DateField(verbose_name='Дата выдачи')),
                ('close_date', models.DateField(verbose_name='Дата окончания')),
                ('visa_type', models.CharField(max_length=20, verbose_name='Тип визы')),
                ('phone_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.Client', verbose_name='Номер телефона')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('number', models.AutoField(primary_key=True, serialize=False)),
                ('departure_time', models.DateTimeField()),
                ('route_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.Route')),
            ],
        ),
        migrations.CreateModel(
            name='SoldTrip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchased_date', models.DateField()),
                ('phone_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.Client')),
                ('trip_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.Trip')),
            ],
        ),
        migrations.CreateModel(
            name='Rest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional', models.TextField(blank=True, verbose_name='Дополнительная информация')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.City', verbose_name='Город')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.Hotel', verbose_name='Отель')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.Route', verbose_name='Маршрут')),
            ],
        ),
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('number', models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='Номер')),
                ('issued_date', models.DateField(verbose_name='Дата выдачи')),
                ('duration', models.PositiveSmallIntegerField(verbose_name='Время действия')),
                ('phone_number', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='trips.Client', verbose_name='Номер телефона клиента')),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.DateTimeField(verbose_name='Время отправления из этой точки маршрута')),
                ('arrival_time', models.DateTimeField(verbose_name='Время прибытия в следующую точку маршрута')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.City', verbose_name='Город')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.Route', verbose_name='Маршрут')),
                ('transport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.Transport', verbose_name='Транспорт')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.Country', verbose_name='Страна'),
        ),
        migrations.CreateModel(
            name='AttendingEvents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.City', verbose_name='Город')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.Event', verbose_name='Мероприятие')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.Route', verbose_name='Маршрут')),
            ],
        ),
    ]
