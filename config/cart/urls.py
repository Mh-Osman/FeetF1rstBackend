# cart/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Cart endpoints
    path('carts/', views.cart_list_create, name='cart-list-create'),
    path('carts/<int:pk>/', views.cart_detail_update, name='cart-detail-update'),

    # Nested Cart Item endpoints
    path('carts/<int:cart_pk>/items/', views.cart_item_list_create, name='cart-item-list-create'),
    path('carts/<int:cart_pk>/items/<int:item_pk>/', views.cart_item_detail_update_delete, name='cart-item-detail-update-delete'),
]