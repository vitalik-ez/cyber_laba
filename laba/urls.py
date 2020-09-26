from django.urls import path

from . import views

urlpatterns = [
    path('', views.test_form, name='laba'),
    path('date', views.date, name='date'),

    path('graphics/', views.FormView.as_view(), name='graphics'),
    path('check_bd/', views.check_bd, name='check_bd'),
    path('check_error/', views.сheck_error, name='check_error'),


    #path('temperature/',views.Plot1DView.as_view(), name='plot1d'),
    #path('temperature_mode/',views.TemperatureMode.as_view(), name='temperature_mode'),
    #path('graph/',views.Graph.as_view(), name='graph'),
    #path('rosa_windy/',views.RosaWindy.as_view(), name='RosaWindy'),
    #path('wind_activity/',views.WindActivity.as_view(), name='WindActivity'),
    #path('test_form/', views.test_form, name='test_form'),
    path('test_form/date', views.date, name='date'),


]


