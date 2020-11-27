from django.urls import path

from . import views

urlpatterns = [
    path('', views.main_form, name='laba'),

    path('graphics/', views.FormView.as_view(), name='graphics'),
    path('check_bd/', views.check_bd, name='check_bd'),
    path('check_error/', views.сheck_error, name='check_error'),

    path('laba2/', views.FormView2.as_view(), name='laba2'),
    path('laba2/clear_session', views.clear_session, name='clear_session'),
    path('laba2/getpdfPageLaba2', views.getpdfPageLaba2, name='getpdfPageLaba2'),

    path('laba3/', views.FormView3.as_view(), name='laba3'),
    path('laba3/add_element', views.FormView3.add_element, name='laba3add'),
    path('laba3/update_element/<int:pk>', views.FormView3.update_element, name='laba3update'),
    path('laba3/delete_element/<int:pk>', views.FormView3.delete_element, name='laba3delete'),
    path('laba3/calculation', views.FormView3.calculation, name='laba3calculation'),


    path('laba4/', views.FormView4.as_view(), name='laba4'),
    path('laba4/getpdfPageLaba4', views.getpdfPageLaba4, name='getpdfPageLaba4'),
    path('laba4/add_element', views.FormView4.add_element, name='laba4add'),
]


