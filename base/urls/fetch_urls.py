from django.urls import path

from base.views import fetch_views as views

urlpatterns = [
    path('get-city/', views.get_city),

    path('get-features/', views.get_features),
    path('get-feature-details/', views.get_feature_details),

    path('filter-color/', views.filter_color),
    path('getcolorimage/', views.color_image),
    path('get-product-features/', views.get_product_features),
    path('get-cities/<int:state_id>/', views.get_cities, name='get_cities'),

    path('pre-order-edit/', views.pre_order_edit),
    path('pre-order-delete/', views.pre_order_delete),
    path('order-complete/', views.order_complete),
    path('order-change-status/', views.order_change_status),
    path('order-delete/', views.order_delete),
    path('order-update/', views.order_update),

    path('get-user-info/', views.get_user_info),

    path('update-status/', views.update_status),

    path('featurevalue-edit/', views.featurevalue_edit),

    path('notification-read/', views.notification_read),
    path('get-color-names/', views.get_color_names)
]
