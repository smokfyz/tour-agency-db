from django.db import models
from django.urls import reverse, resolve


class Country(models.Model):
    # Fields
    name = models.CharField(primary_key=True, max_length=255, verbose_name = 'Название')
    visa_required = models.BooleanField(verbose_name = 'Обязательность визы')
    passport_required = models.BooleanField(verbose_name = 'Обязательность загранпаспорта')
    visa_price = models.PositiveIntegerField(blank=True, null=True, verbose_name = 'Цена визы')
    passport_price = models.PositiveIntegerField(blank=True, null=True, verbose_name = 'Цена загранпаспорта')

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return str(self.name)


class Client(models.Model):
    # Fields
    phone_number = models.CharField(primary_key=True, max_length=20, verbose_name = 'Номер телефона')
    reg_date = models.DateField(verbose_name = 'Дата регистрации')
    passport_num = models.PositiveIntegerField(verbose_name = 'Номер паспорта')
    passport_ser = models.PositiveIntegerField(verbose_name = 'Серия паспорта')
    surname = models.CharField(max_length=20, verbose_name = 'Фамилия')
    name = models.CharField(max_length=20, verbose_name = 'Имя')
    mid_name = models.CharField(max_length=20, verbose_name = 'Отчество')
    issued_by = models.TextField(verbose_name = 'Кем выдан паспорт')
    issued_date = models.DateField(verbose_name = 'Дата выдачи пасспорта')
    birth_date = models.DateField(verbose_name = 'Дата рождения')
    citizenship = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name = 'Гражданство')
    region = models.CharField(max_length=50, blank=True, verbose_name = 'Регион')
    city = models.CharField(max_length=20, verbose_name = 'Город')
    street = models.CharField(max_length=100, verbose_name = 'Улица')
    house = models.PositiveSmallIntegerField(verbose_name = 'Дом')
    corpus = models.CharField(max_length=2, blank=True, verbose_name = 'Корпус')
    flat = models.PositiveSmallIntegerField(verbose_name = 'Квартира')
    zip_code = models.PositiveIntegerField(verbose_name = 'Индекс')
    notes = models.TextField(blank=True, verbose_name = 'Замечания')
    
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return str(self.phone_number)

    def get_absolute_url(self):
        return u'/clients/%s' % str(self.phone_number)


class Passport(models.Model):
    # Fields
    number = models.PositiveIntegerField(primary_key=True, verbose_name = 'Номер')
    issued_date = models.DateField(verbose_name = 'Дата выдачи')
    duration= models.PositiveSmallIntegerField(verbose_name = 'Время действия')
    phone_number = models.OneToOneField(Client, on_delete=models.CASCADE, verbose_name = 'Номер телефона клиента')
    
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return str(self.number)

    def get_absolute_url(self):
        return u'/clients/%s/passport/' % str(self.phone_number)


class Visa(models.Model):
    # Fields
    number = models.PositiveIntegerField(primary_key=True, verbose_name = 'Номер визы')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name = 'Страна')
    issued_date = models.DateField(verbose_name = 'Дата выдачи')
    close_date = models.DateField(verbose_name = 'Дата окончания')
    visa_type = models.CharField(max_length=20, verbose_name = 'Тип визы')
    phone_number = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name = 'Номер телефона')

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return str(self.number)

    def get_absolute_url(self):
        return u'/clients/%s/visas/%s/' %(str(self.phone_number), str(self.number))


class Transport(models.Model):
    # Fields
    name = models.CharField(primary_key=True, max_length=50, verbose_name = 'Тип транспорта')
    
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return str(self.name)



class Hotel(models.Model):
    # Fields
    name = models.CharField(primary_key=True, max_length=255, verbose_name = 'Название')
    description = models.TextField(verbose_name = 'Описание')
    
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return str(self.name)


class Event(models.Model):
    # Fields
    name = models.CharField(max_length=255, verbose_name = 'Наименование')
    description = models.TextField(verbose_name = 'Описание')

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return str(self.name)


class City(models.Model):
    # Fields
    name = models.CharField(primary_key=True, max_length=255, verbose_name = 'Название')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name = 'Страна')
    
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return str(self.name)


class Route(models.Model):
    # Fields
    number = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name = 'Название маршрута')
    description = models.TextField(verbose_name = 'Описание маршрута')
    price = models.PositiveIntegerField(verbose_name = 'Цена')
    duration = models.PositiveIntegerField(verbose_name = 'Длительность')
    
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return str(self.name)

    def get_absolute_url(self):
        return u'/trips/route/%s/' %(str(self.number))


class Move(models.Model):
    # Fields
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name = 'Маршрут')
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, verbose_name = 'Транспорт')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name = 'Город')
    departure_time = models.DateTimeField(verbose_name = 'Время отправления из этой точки маршрута')
    arrival_time = models.DateTimeField(verbose_name = 'Время прибытия в следующую точку маршрута')

    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return str(self.route)

    def get_absolute_url(self):
        return u'/trips/route/%s/moves/%s/' %(str(self.route.number), str(self.id))


class Rest(models.Model):
    # Fields
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name = 'Маршрут')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name = 'Отель')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name = 'Город')
    additional = models.TextField(blank=True, verbose_name = 'Дополнительная информация')
    
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return str(self.hotel)


class AttendingEvents(models.Model):
    # Fields
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name = 'Маршрут')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name = 'Мероприятие')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name = 'Город')
    
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return str(self.event)


class Trip(models.Model):
    # Fields
    number = models.AutoField(primary_key=True, verbose_name = 'Номер путевки')
    route_name = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name = 'Маршрут')
    departure_time = models.DateTimeField(verbose_name = 'Время отправления')
    
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return str(self.number)


class SoldTrip(models.Model):
    # Fields
    phone_number = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name = 'Номер телефона')
    trip_number = models.ForeignKey(Trip, on_delete=models.CASCADE, verbose_name = 'Номер путевки')
    purchased_date = models.DateField(verbose_name = 'Дата продажи')
    
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return str(self.trip_number)


class Discount(models.Model):
    # Fields
    bought = models.PositiveIntegerField(verbose_name = 'Количество купленных путевок', unique=True)
    discount = models.PositiveIntegerField(verbose_name = 'Размер скидки(%)')
    
    def __str__(self):
        """
        String for representing the MyModelName object (in Admin site etc.)
        """
        return str(self.id)

    def get_absolute_url(self):
        return u'/discount/%s' % str(self.id)