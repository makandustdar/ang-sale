from django.urls import path
from users.views import expert_views as views


urlpatterns = [
    path('list/', views.ExpertList.as_view(), name='expert_list'),
    path('add/', views.add, name='expert_add'),
    path('edit/<expert_id>/', views.edit, name='expert_edit'),
    path('transfer_customers/<int:expert_id>/', views.transfer_customers, name='transfer_customers')
]
