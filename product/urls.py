from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.ProductList.as_view(), name='product_list'),
    path('add/', views.add, name="product_add"),
    path('edit/<productId>/', views.edit, name='product_edit'),

    path('feature-list/', views.FeatureList.as_view(), name='feature_list'),
    path('feature-add/', views.feature_add, name="feature_add"),
    path('feature-edit/<featureId>/', views.feature_edit, name='feature_edit'),
    path('feature-value-add/<int:feature_id>/', views.feature_value_add, name='feature_value_add'),

    path('color/list/', views.ColorList.as_view(), name='color_list'),
    path('color/add/', views.color_add, name='color_add'),
    path('color/edit/<colorId>/', views.color_edit, name='color_edit'),
    path('color/delete/<color_id>/', views.color_delete, name='delete_color'),

]
