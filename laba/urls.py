from django.urls import path

from . import views

urlpatterns = [
    path('', views.test_form, name='laba'),

    path('graphics/', views.FormView.as_view(), name='graphics'),
    path('check_bd/', views.check_bd, name='check_bd'),
    path('check_error/', views.сheck_error, name='check_error'),

]


