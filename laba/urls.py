from django.urls import path

from . import views

urlpatterns = [
    path('', views.main_form, name='laba'),

    path('graphics/', views.FormView.as_view(), name='graphics'),
    path('check_bd/', views.check_bd, name='check_bd'),
    path('check_error/', views.сheck_error, name='check_error'),

    path('laba2/', views.FormView2.as_view(), name='laba2'),
    path('laba2/clear_file', views.clear_file, name='clear_file'),

]


