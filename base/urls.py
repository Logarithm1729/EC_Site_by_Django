from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


app_name = 'base'

urlpatterns = [
    # Top-page
    path('', views.IndexView.as_view(), name='index'),

    # Items
    path('items/<str:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('categories/<str:pk>/', views.CategoryListView.as_view(), name='categories'),
    path('tags/<str:pk>/', views.TagListView.as_view(), name='tags'),

    # Cart
    path('cart/', views.CartListView.as_view(), name='cart_list'),
    path('cart/add/', views.AddCartView.as_view(), name='cart_add'),
    path('cart/remove/<str:pk>/', views.remove_item_from_cart, name='cart_remove'),

    # Pay
    path('pay/checkout/', views.create_checkout_session, name='checkout'),
    path('pay/success/', views.SuccessView.as_view(), name='success'),
    path('pay/cancel/', views.CancelView.as_view(), name='cancel'),

    # Account
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path('account/', views.AccountUpdateView.as_view(), name='account'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),

    # Order
    path('orders/<str:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/', views.OrderIndexView.as_view(), name='order_list'),
]