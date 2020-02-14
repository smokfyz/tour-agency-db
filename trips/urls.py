from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('home/', views.index, name='index'),
    path('clients/', views.clients, name='clients'),
    path('trips/', views.trips, name='trips'),
    path('reports/', views.reports, name='reports'),
    path('discount/', views.discount, name='discount'),
    url(r'sold/(?P<pk>[-\w]+)/', views.detail_to_pdf, name='trip-sold'),
]

urlpatterns += [   
    url(r'^discount/add/$', views.DiscountCreate.as_view(), name='client-page'),
    url(r'^discount/(?P<pk>[-\w]+)/delete/$', views.DiscountDelete.as_view(), name='client-page'),
    url(r'^discount/(?P<pk>[-\w]+)/update/$', views.DiscountUpdate.as_view(), name='client-page'),
]

urlpatterns += [   
    url(r'^reports/month/$', views.month_report, name='client-page'),
    url(r'^reports/best/$', views.best_report, name='client-page'),
]

urlpatterns += [   
    url(r'^clients/(?P<pk>[-\w]+)/$', views.ClientUpdate.as_view(), name='client-page'),
    url(r'^clients/(?P<pk>[-\w]+)/create/$', views.ClientCreate.as_view(), name='client-create'),
    url(r'^clients/(?P<pk>[-\w]+)/create/country/$', views.CountryCreate.as_view(), name='country-create'),
]

urlpatterns += [
    url(r'^clients/(?P<pk>[-\w]+)/visas/$', views.VisasListView.as_view(), name='client-visas'),
    url(r'^clients/(?P<pk>[-\w]+)/visas/create/$', views.VisaCreate.as_view(), name='client-visas-create'),
    url(r'^clients/(?P<pk>[-\w]+)/visas/(?P<num>[-\w]+)/$', views.VisaUpdate.as_view(), name='client-visa'),
    url(r'^clients/(?P<pk>[-\w]+)/passport/$', views.PassportUpdate.as_view(), name='client-passport'),
    url(r'^clients/(?P<pk>[-\w]+)/passport/create/$', views.PassportCreate.as_view(), name='client-passport-create'),
]

urlpatterns += [
    url(r'^trips/list/$', views.TripsListView.as_view(), name='trips-list'),
    url(r'^trips/route/create/$', views.RouteCreate.as_view(), name='route-create'),
    url(r'^trips/route/$', views.RouteListView.as_view(), name='route-list'),
    url(r'^trips/route/(?P<pk>[-\w]+)/$', views.RouteUpdate.as_view(), name='route-create'),
    url(r'^trips/route/(?P<pk>[-\w]+)/moves/add/$', views.MoveCreate.as_view(), name='move-create'),
    url(r'^trips/route/(?P<pk>[-\w]+)/moves/(?P<id>[-\w]+)/delete/$', views.MoveDelete.as_view(), name='move-delete'),
    url(r'^trips/route/(?P<pk>[-\w]+)/moves/(?P<id>[-\w]+)/$', views.MoveUpdate.as_view(), name='move-update'),
    url(r'^trips/route/(?P<pk>[-\w]+)/moves/add/transport/$', views.TransportCreate.as_view(), name='transport-create'),
    url(r'^trips/route/(?P<pk>[-\w]+)/moves/add/city/$', views.CityCreate.as_view(), name='city-create'),
    url(r'^trips/route/(?P<pk>[-\w]+)/moves/add/city/country/$', views.CountryCreate.as_view(), name='country-create'),
    url(r'^trips/route/(?P<pk>[-\w]+)/moves/(?P<id>[-\w]+)/transport/$', views.TransportCreate.as_view(), name='transport-create'),
    url(r'^trips/route/(?P<pk>[-\w]+)/moves/(?P<id>[-\w]+)/city/$', views.CityCreate.as_view(), name='city-create'),
    url(r'^trips/route/(?P<pk>[-\w]+)/moves/(?P<id>[-\w]+)/city/country/$', views.CountryCreate.as_view(), name='country-create'),
    url(r'^trips/route/(?P<pk>[-\w]+)/moves/(?P<id>[-\w]+)/events/$', views.AttendingEventsCreate.as_view(), name='events-create'),
    url(r'^trips/route/(?P<pk>[-\w]+)/moves/(?P<id>[-\w]+)/events/(?P<num>[-\w]+)/delete/$', views.AttendingEventsDelete.as_view(), name='events-delete'),
    url(r'^trips/route/(?P<pk>[-\w]+)/moves/(?P<id>[-\w]+)/events/add/$', views.EventCreate.as_view(), name='events-create'),
    url(r'^trips/route/(?P<pk>[-\w]+)/moves/(?P<id>[-\w]+)/hotel/$', views.RestCreate.as_view(), name='hotels-create'),
    url(r'^trips/route/(?P<pk>[-\w]+)/moves/(?P<id>[-\w]+)/hotel/add/$', views.HotelCreate.as_view(), name='hotels-create'),
    url(r'^trips/route/(?P<pk>[-\w]+)/moves/(?P<id>[-\w]+)/hotel-update/$', views.RestUpdate.as_view(), name='hotels-create'),
    url(r'^trips/route/(?P<pk>[-\w]+)/moves/(?P<id>[-\w]+)/hotel-update/add/$', views.HotelCreate.as_view(), name='hotels-create')
]

urlpatterns += [
    url(r'^trips/release-trips/$', views.TripCreate.as_view(), name='trips-release'),
    url(r'^sale-trips/(?P<pk>[-\w]+)/$', views.SoldTripCreate.as_view(), name='sale-trips'),
]