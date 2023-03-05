from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('part_info', views.part_info, name='part_info'),
    path('register/', views.register, name='register'),
    path('part_info/', views.part_info, name='part_info'),
]