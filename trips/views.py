from django.shortcuts import render
from .models import Client, Passport, Visa, Trip, Route, Move, Transport, City, Country, Hotel, AttendingEvents, Event, Rest, SoldTrip, Discount
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, resolve
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.forms import DateInput
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.admin.widgets import AdminDateWidget
from django.db.models import Count, Value
from django.db import models

import datetime

from .forms import GetClient, CreateClient, TripFilter
from easy_pdf.rendering import render_to_pdf_response


def index(request):
    return render(
        request,
        'index.html'
    )


def clients(request):
    if request.method == 'POST':
        if request.POST.get("find"):
            form = GetClient(request.POST)
            if form.is_valid():
                return HttpResponseRedirect(form.cleaned_data['phone_number'])

        elif request.POST.get("create"):
            form = CreateClient(request.POST)
            if form.is_valid():
                return HttpResponseRedirect(form.cleaned_data['phone_number'] + "/create")

    else:
        form = GetClient()

    return render(request, 'clients.html', {'form': form})


def trips(request):
    return render(
        request,
        'trips.html',
    )


def reports(request):
    return render(
        request,
        'reports.html',
    )


def discount(request):
    discount = Discount.objects.all()
    return render(
        request,
        'discount.html',
        {
            'discount': discount
        }
    )


class ClientUpdate(SuccessMessageMixin, UpdateView):
    model = Client
    fields = '__all__'
    template_name_suffix = '-page'
    success_message = "Информация о клиенте обновлена!"

    def get_context_data(self, **kwargs):
        context = super(ClientUpdate, self).get_context_data(**kwargs)
        passport = Passport.objects.filter(phone_number=self.kwargs['pk'])
        if passport:
            context['passport_exist'] = True
        else:
            context['passport_exist'] = False
        return context


class ClientCreate(SuccessMessageMixin, CreateView):
    model = Client
    fields = '__all__'
    template_name_suffix = '-page-create'
    success_message = "Клиент добавлен в базу данных!"

    def get_initial(self):
        return {'phone_number': self.kwargs['pk']}
    
    def get_form(self):
        form = super().get_form()
        return form


class PassportUpdate(SuccessMessageMixin, UpdateView):
    model = Passport
    fields = '__all__'
    template_name_suffix = '-page'
    success_message = "Информация о загранпаспорте обновлена!"

    def get_object(self):
        return get_object_or_404(Passport, phone_number=self.kwargs['pk'])


class PassportCreate(SuccessMessageMixin, CreateView):
    model = Passport
    fields = '__all__'
    template_name_suffix = '-page-create'
    success_message = "Загранпаспорт успешно оформлен!"

    def get_initial(self):
        return {'phone_number': self.kwargs['pk']}
    
    def get_form(self):
        form = super().get_form()
        return form


class VisaUpdate(SuccessMessageMixin, UpdateView):
    model = Visa
    fields = '__all__'
    template_name_suffix = '-page'
    success_message = "Информация о визе обновлена!"

    def get_object(self):
        return get_object_or_404(Visa, phone_number=self.kwargs['pk'], number=self.kwargs['num'])


class VisaCreate(SuccessMessageMixin, CreateView):
    model = Visa
    fields = '__all__'
    template_name_suffix = '-page-create'
    success_message = "Виза успешно оформлена!"

    def get_initial(self):
        return {'phone_number': self.kwargs['pk'], 'of': self.kwargs['pk']}
    
    def get_form(self):
        form = super().get_form()
        return form


class VisasListView(generic.ListView):
    model = Visa
    context_object_name = 'visas_list'
    template_name_suffix = '-list'

    def get_queryset(self):
        return Visa.objects.filter(phone_number=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(VisasListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context


class TripsListView(generic.ListView):
    model = Trip
    context_object_name = 'trips_list'
    template_name_suffix = '-list'

    def get_queryset(self):
        sold = SoldTrip.objects.all()
        trips = Trip.objects.all()

        for trip in sold:
            trips = trips.exclude(number=trip.trip_number.number)

        trips_uniq = trips.values('route_name').annotate(count=Count('number'))

        items = set()
        for trip_uniq in trips_uniq:
            for trip in trips:
                if trip.route_name.number == trip_uniq['route_name']:
                    items.add(trip.number)
                    break

        trips = trips.filter(number__in=items)

        self.f = TripFilter(self.request.GET, queryset=trips)

        return trips

    def get_context_data(self, **kwargs):
        context = super(TripsListView, self).get_context_data(**kwargs)

        sold = SoldTrip.objects.all()
        trips = Trip.objects.all()

        for trip in sold:
            trips = trips.exclude(number=trip.trip_number.number)

        trips_uniq = trips.values('route_name').annotate(count=Count('number'))

        context['trips_count'] = list(trips_uniq)
        context['filter'] = self.f
        return context


class RouteUpdate(SuccessMessageMixin, UpdateView):
    model = Route
    fields = '__all__'
    template_name_suffix = '-page'
    success_message = "Информация о маршруте обновлена!"

    def get_object(self):
        return get_object_or_404(Route, number=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(RouteUpdate, self).get_context_data(**kwargs)
        moves = Move.objects.filter(route=self.kwargs['pk'])
        events = AttendingEvents.objects.filter(route=self.kwargs['pk'])
        hotels = Rest.objects.filter(route=self.kwargs['pk'])
        context['moves'] = moves
        context['events'] = events
        context['hotels'] = hotels
        return context


class RouteCreate(SuccessMessageMixin, CreateView):
    model = Route
    fields = '__all__'
    template_name_suffix = '-page-create'
    success_message = "Маршрут успешно создан!"
    
    def get_form(self):
        form = super().get_form()
        return form


class RouteListView(generic.ListView):
    model = Route
    context_object_name = 'routes_list'
    template_name_suffix = '-list'

    def get_queryset(self):
        return Route.objects.all()

    def get_context_data(self, **kwargs):
        context = super(RouteListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context


class MoveUpdate(SuccessMessageMixin, UpdateView):
    model = Move
    fields = '__all__'
    template_name_suffix = '-page'
    success_message = "Информация о точке маршрута обновлена!"

    def get_object(self):
        return get_object_or_404(Move, id=self.kwargs['id'])

    def get_success_url(self):
        return '../../'


class MoveCreate(SuccessMessageMixin, CreateView):
    model = Move
    fields = '__all__'
    template_name_suffix = '-page-create'
    success_message = "Точка маршрута успешно создана!"

    def get_initial(self):
        return {'route': self.kwargs['pk']}

    def get_form(self):
        form = super(MoveCreate, self).get_form()
        return form

    def get_success_url(self):
        return '../../'
        

class TransportCreate(SuccessMessageMixin, CreateView):
    model = Transport
    fields = '__all__'
    template_name_suffix = '-page-create'
    success_message = "Транспорт успешно создан!"

    def get_initial(self):
        return {'route': self.kwargs['pk']}

    def get_form(self):
        form = super(TransportCreate, self).get_form()
        return form

    def get_success_url(self):
        return '../'


class CityCreate(SuccessMessageMixin, CreateView):
    model = City
    fields = '__all__'
    template_name_suffix = '-page-create'
    success_message = "Город успешно добавлен!"

    def get_initial(self):
        return {'route': self.kwargs['pk']}

    def get_form(self):
        form = super(CityCreate, self).get_form()
        return form

    def get_success_url(self):
        return '../'


class CountryCreate(SuccessMessageMixin, CreateView):
    model = Country
    fields = '__all__'
    template_name_suffix = '-page-create'
    success_message = "Страна успешно добавлена!"

    def get_initial(self):
        return {'route': self.kwargs['pk']}

    def get_form(self):
        form = super(CountryCreate, self).get_form()
        return form

    def get_success_url(self):
        return '../'


class MoveDelete(SuccessMessageMixin, DeleteView):
    model = Move
    fields = '__all__'
    template_name_suffix = '-page-delete'
    success_message = "Точка маршрута успешно удалена!"

    def get_object(self):
        return get_object_or_404(Move, id=self.kwargs['id'])

    def get_form(self):
        form = super(MoveDelete, self).get_form()
        return form

    def get_success_url(self):
        return '../../../'


class AttendingEventsCreate(SuccessMessageMixin, CreateView):
    model = AttendingEvents
    fields = '__all__'
    template_name_suffix = '-page-create'
    success_message = "Посещение меропиятия успешно добавлено!"

    def get_initial(self):
        city = Move.objects.filter(id=self.kwargs['id'])[0].city
        return {'route': self.kwargs['pk'], 'city': city}

    def get_form(self):
        form = super(AttendingEventsCreate, self).get_form()
        return form

    def get_success_url(self):
        return '../../../'


class AttendingEventsDelete(SuccessMessageMixin, DeleteView):
    model = AttendingEvents
    fields = '__all__'
    template_name_suffix = '-page-delete'
    success_message = "Посещение мероприятия успешно удалено!"

    def get_object(self):
        return get_object_or_404(AttendingEvents, id=self.kwargs['num'])

    def get_form(self):
        form = super(AttendingEventsDelete, self).get_form()
        return form

    def get_success_url(self):
        return '../../../../../'


class EventCreate(SuccessMessageMixin, CreateView):
    model = Event
    fields = '__all__'
    template_name_suffix = '-page-create'
    success_message = "Мероприятие успешно добавлено!"

    def get_initial(self):
        return {'route': self.kwargs['pk']}

    def get_form(self):
        form = super(EventCreate, self).get_form()
        return form

    def get_success_url(self):
        return '../'



class RestCreate(SuccessMessageMixin, CreateView):
    model = Rest
    fields = '__all__'
    template_name_suffix = '-page-create'
    success_message = "Отдых в отеле успешно добавлено!"

    def get_initial(self):
        city = Move.objects.filter(id=self.kwargs['id'])[0].city
        return {'route': self.kwargs['pk'], 'city': city}

    def get_form(self):
        form = super(RestCreate, self).get_form()
        return form

    def get_success_url(self):
        return '../../../'



class HotelCreate(SuccessMessageMixin, CreateView):
    model = Hotel
    fields = '__all__'
    template_name_suffix = '-page-create'
    success_message = "Отель успешно добавлен!"

    def get_initial(self):
        return {'route': self.kwargs['pk']}

    def get_form(self):
        form = super(HotelCreate, self).get_form()
        return form

    def get_success_url(self):
        return '../'


class RestUpdate(SuccessMessageMixin, UpdateView):
    model = Rest
    fields = '__all__'
    template_name_suffix = '-page'
    success_message = "Информация об отдыхе в отеле обновлена!"

    def get_object(self):
        city = Move.objects.filter(id=self.kwargs['id'])[0].city
        return get_object_or_404(Rest, route=self.kwargs['pk'], city=city)

    def get_context_data(self, **kwargs):
        context = super(RestUpdate, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return '../../../'


class TripCreate(SuccessMessageMixin, CreateView):
    model = Trip
    fields = '__all__'
    template_name_suffix = '-page-create'
    success_message = "Путевки успешно добавлены!"

    def get_form(self):
        form = super(TripCreate, self).get_form()
        return form

    def get_success_url(self):
        return '../'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class SoldTripCreate(SuccessMessageMixin, CreateView):
    model = SoldTrip
    fields = '__all__'
    template_name_suffix = '-page-create'
    success_message = "Путевка успешно продана!"

    def get_form(self):
        form = super(SoldTripCreate, self).get_form()
        form.fields['trip_number'].widget.attrs['readonly'] = True
        form.fields['purchased_date'].widget.attrs['readonly'] = True
        return form

    def get_success_url(self):
        form = self.get_form()
        return '/sold/' + str(form.data['trip_number'])

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_initial(self):
        return {'trip_number': self.kwargs['pk'], 'purchased_date': datetime.datetime.now()}


def detail_to_pdf(request, pk):
    template = 'reports/sold.html'
    trip_sold = SoldTrip.objects.get(trip_number=pk)

    client = Client.objects.get(phone_number=trip_sold.phone_number)

    discounts = list(Discount.objects.all().values())
    discounts.sort(key=lambda x: -x['discount'])

    bought_trips = len(SoldTrip.objects.filter(phone_number=client))

    price = trip_sold.trip_number.route_name.price
    discount = 0
    for dis in discounts:
        if bought_trips >= dis['bought']:
            price = int(price*(1 - dis['discount']/100))
            discount = dis['discount']
            break

    moves = Move.objects.filter(route=trip_sold.trip_number.route_name)

    needed_passport = False
    for move in moves:
        if move.city.country.passport_required:
            needed_passport = True
            break

    passport_price = 0
    if not Passport.objects.filter(phone_number=client) and needed_passport and client.citizenship.passport_price and client.citizenship.passport_required:
        passport_price = client.citizenship.passport_price

    visas = Visa.object.filter(phone_number=client)
    visas_required = []

    for move in moves:
        if move.city.country.visa_required and not visas.filter(country=move.city.country):
            visas_required.append({
                'country': move.city.country,
                'price': move.city.country.visa_price
            })

    events = AttendingEvents.objects.filter(route=trip_sold.trip_number.route_name)
    hotels = Rest.objects.filter(route=trip_sold.trip_number.route_name)
    context = {
        'moves': moves,
        'events': events,
        'hotels': hotels,
        'trip_sold': trip_sold,
        'price': price,
        'discount': discount,
        'passport_price': passport_price,
        'needed_passport': needed_passport,
        'visas_required': visas_required,
    }
    return render_to_pdf_response(request, template, context, content_type='application/pdf', encoding ="utf-8")


def month_report(request):
    template = 'reports/month.html'
    date_now = datetime.datetime.now()
    date_month = datetime.datetime(date_now.year, date_now.month, 1)

    sold_trips = SoldTrip.objects.filter(purchased_date__lte=date_now, purchased_date__gte=date_month).values('trip_number')
    sold_trips = Trip.objects.filter(number__in=sold_trips)

    routes = Route.objects.all()
    trips_count_by_route = sold_trips.values('route_name').annotate(Count('route_name'))
    
    sold_info = []
    for trips_cbr in trips_count_by_route:
        sold_info.append({
            'route': routes.get(number=trips_cbr['route_name']),
            'count': trips_cbr['route_name__count']
        })

    best_sold = sold_info
    best_sold.sort(key=lambda x: -x['count'])
    leng = int(len(best_sold)/2)
    best_sold = best_sold[0:leng]

    sold_trips = Trip.objects.exclude(number__in=sold_trips)
    routes = Route.objects.all()
    trips_count_by_route = sold_trips.values('route_name').annotate(Count('route_name'))
    
    sold_info_bad = []
    for trips_cbr in trips_count_by_route:
        sold_info_bad.append({
            'route': routes.get(number=trips_cbr['route_name']),
            'count': trips_cbr['route_name__count']
        })
    print(sold_info_bad)
    total_price = 0
    for trip in sold_trips:
        total_price = total_price + trip.route_name.price

    context = {
        'sold_info': sold_info,
        'total_price': total_price,
        'best_sold': best_sold,
        'bad_sold': sold_info_bad,
        'date_month': date_month
    }
    return render_to_pdf_response(request, template, context, content_type='application/pdf', encoding ="utf-8")


def best_report(request):
    template = 'reports/best.html'

    sold_trips = SoldTrip.objects.values('trip_number')
    sold_trips = Trip.objects.filter(number__in=sold_trips)

    routes = Route.objects.all()
    trips_count_by_route = sold_trips.values('route_name').annotate(Count('route_name'))
    
    sold_info = []
    for trips_cbr in trips_count_by_route:
        sold_info.append({
            'route': routes.get(number=trips_cbr['route_name']),
            'count': trips_cbr['route_name__count']
        })

    sold_info.sort(key=lambda x: -x['count'])

    context = {
        'sold_info': sold_info,
    }
    return render_to_pdf_response(request, template, context, content_type='application/pdf', encoding ="utf-8")


class DiscountCreate(SuccessMessageMixin, CreateView):
    model = Discount
    fields = '__all__'
    template_name_suffix = '-page-create'
    success_message = "Скидка добавлена в базу данных!"
    
    def get_success_url(self):
        form = self.get_form()
        return '../'

    def get_form(self):
        form = super().get_form()
        return form


class DiscountUpdate(SuccessMessageMixin, UpdateView):
    model = Discount
    fields = '__all__'
    template_name_suffix = '-page'
    success_message = "Информация о скидке обновлена!"

    def get_success_url(self):
        return '../../'


class DiscountDelete(SuccessMessageMixin, DeleteView):
    model = Discount
    fields = '__all__'
    template_name_suffix = '-page-delete'
    success_message = "Скидка успешно удалена!"

    def get_object(self):
        return get_object_or_404(Discount, id=self.kwargs['pk'])

    def get_form(self):
        form = super(DiscountDelete, self).get_form()
        return form

    def get_success_url(self):
        return '../../'