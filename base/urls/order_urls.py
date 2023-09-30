from django.urls import path
from base.views import order_views as views

urlpatterns = [
    path('list/', views.OrderList.as_view(), name='order_list'),
    path('add/', views.add, name="order_add"),
    path('submit_order/', views.submit_order, name='submit_order'),
    path('edit/<orderId>/', views.edit, name="order_edit"),
    path('detail/<order_id>/', views.detail, name='order_detail'),
    path('invoice/<order_id>/', views.invoice, name='order_invoice'),
    path('update/<int:item_id>/', views.update_fee_or_quantity, name='update_fee_or_quantity'),
    path('admin/list/', views.AdminOrderList.as_view(), name='admin_order_list'),
    path('admin/add/', views.admin_add, name="admin_order_add"),
    path("admin/prices/", views.set_order_price, name='set_order_price'),
    path("admin/items/prices/", views.change_items_price, name='change_items_price'),

    path('delete/<int:pk>/', views.OrderDeleteAdminView.as_view(), name='delete_order_admin'),
    path('check-code/<int:order_id>/', views.check_confirmation_is_ok, name='check_confirmation_is_ok'),
]
