from django.urls import path
from partsApp.views import PartDetailView, HomeView, add_to_cart, remove_from_cart, CartSummaryView, Checkout, \
    remove_single_part_from_cart

from . import views

app_name = 'partsApp'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('part/<slug>/', PartDetailView.as_view(), name='part'),
    path('cart_summary/', CartSummaryView.as_view(), name='cart_summary'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('remove_single_part_from_cart/<slug>/', remove_single_part_from_cart, name='remove_single_part_from_cart'),
    path('checkout/', Checkout.as_view(), name='checkout')

]