from django.contrib import admin
from .models import (
    Client, 
    Passport, 
    Visa, 
    Transport, 
    Hotel, 
    Event, 
    Country, 
    City, 
    Route, 
    Move, 
    Rest, 
    AttendingEvents, 
    Trip, 
    SoldTrip
)

admin.site.register(Client)
admin.site.register(Passport)
admin.site.register(Visa)
admin.site.register(Transport)
admin.site.register(Hotel)
admin.site.register(Event)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Route)
admin.site.register(Move)
admin.site.register(Rest)
admin.site.register(AttendingEvents)
admin.site.register(Trip)
admin.site.register(SoldTrip)
