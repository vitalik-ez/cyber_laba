from django.urls import path

from . import views

urlpatterns = [
    path('',views.IndexView.as_view(), name='index'),
    path('form/', views.FormView.as_view(), name='form'),
    path('check_bd/', views.check_bd, name='check_bd'),


    #path('temperature/',views.Plot1DView.as_view(), name='plot1d'),
    #path('temperature_mode/',views.TemperatureMode.as_view(), name='temperature_mode'),
    path('graph/',views.Graph.as_view(), name='graph'),

    path('get_name/', views.get_name, name='get_name'),
    path('show_name/', views.show_name, name='show_name'),
    path('show_name/<slug:username>', views.show_name, name='show_name'),
    path('new/', views.new, name='new'),

]


