from django.urls import path
from partsApp.views import Cart, Index

from . import views

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('login/', views.login_view, name='login'),
    # path('part_info', views.part_info, name='part_info'),
    path('register/', views.register, name='register'),
    # path('part_info/', views.part_info, name='part_info'),
    path('cart/', Cart.as_view(), name='cart'),
]