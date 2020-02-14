from django import forms
from .models import Client, Passport, Visa
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
import django_filters
from .models import Client, Passport, Visa, Trip, Route, Move, Transport, City, Country, Hotel, AttendingEvents, Event, Rest, SoldTrip
from django.utils import timezone
import pytz


class GetClient(forms.Form):
    phone_number = forms.CharField(error_messages = {
        'required': 'Данное поле является обязательным.',
        'invalid': 'Введите корректное значение.'
    })
    phone_number.label = "Номер телефона"

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        
        if len(data) != 11:
            raise ValidationError(_('Неверный формат номера. Пример: 79312852172.'))

        client_inst = Client.objects.filter(pk=data)

        if not client_inst:
            raise ValidationError(_('Клиент не найден.'))

        return data

    def form_valid(self, form):
        self.object = form.save()
        return self.render_to_response(self.get_context_data(form=form))


class CreateClient(forms.Form):
    phone_number = forms.CharField(error_messages = {
        'required': 'Данное поле является обязательным.',
        'invalid': 'Введите корректное значение.'
    })
    phone_number.label = "Номер телефона"

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        
        if len(data) != 11:
            raise ValidationError(_('Неверный формат номера. Пример: 79312852172.'))

        client_inst = Client.objects.filter(pk=data)

        if client_inst:
            raise ValidationError(_('Клиент с таким номером уже существует.'))

        return data

    def form_valid(self, form):
        self.object = form.save()
        return self.render_to_response(self.get_context_data(form=form))
    

class TripFilter(django_filters.FilterSet):
    route_name__price__gte = django_filters.NumberFilter(field_name='route_name', lookup_expr='price__gte', label='Минимальная цена')
    route_name__price__lte = django_filters.NumberFilter(field_name='route_name', lookup_expr='price__lte', label='Максимальная цена')
    country = django_filters.ModelChoiceFilter(queryset=Country.objects.all(), method='search_trips_by_countries', label='Страна')
    date_range = django_filters.DateTimeFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy-mm-dd hh:mm'}), 
                                                          method='search_trips_by_range', label="Сроки")
    transport = django_filters.ModelChoiceFilter(queryset=Transport.objects.all(), method='exclude_transport', label='Исключить транспорт')
    hot_trips = django_filters.BooleanFilter(field_name='hot_trips', method='show_hot_trips', label='Горячие путевки')
    order_f = django_filters.OrderingFilter(label='Сортировка',
        fields=(
            ('route_name__price', 'route_name__price'),
        ),
        field_labels={
            'route_name__price': 'Цена',
        })

    class Meta:
        model = Trip
        fields = ['route_name__price__gte', 'route_name__price__lte', 'country', 'date_range', 'transport',
        'hot_trips', 'order_f']

    def search_trips_by_countries(self, queryset, name, value):
        routes = queryset.values('route_name')
        moves = Move.objects.filter(route__in=routes).filter(city__country=value)
        return queryset.filter(route_name__in=moves.values('route'))

    def search_trips_by_range(self, queryset, name, value):
        routes = queryset.values('route_name')
        moves = Move.objects.filter(route__in=routes).order_by('departure_time')
        start_date = value.start
        stop_date = value.stop
        country = self.form.cleaned_data['country']

        departure_time = None
        arrival_time = None
        new_move = moves
        for move in moves:
            departure_time = move.departure_time
            if arrival_time and (not country or country and country == move.city.country) \
                and arrival_time <= start_date and stop_date <= departure_time:
                pass
            else:
                new_move = new_move.exclude(id=move.id)
            arrival_time = move.arrival_time

        return queryset.filter(route_name__in=new_move.values('route'))

    def exclude_transport(self, queryset, name, value):
        routes = queryset.values('route_name')
        moves = Move.objects.filter(route__in=routes)

        new_move = moves.filter(transport=value)

        return queryset.exclude(route_name__in=new_move.values('route'))

    def show_hot_trips(self, queryset, name, value):
        now = datetime.datetime.now()
        now += datetime.timedelta(days=5)

        if value:
            return queryset.filter(departure_time__lte=now)
        else:
            return queryset.exclude(departure_time__lte=now)