from django.urls import path

from base.views import base_views as views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile'),
    path('user/', views.dashboard_user, name="dashboard_user"),
    path('admin/', views.dashboard_admin, name='dashboard_admin'),
    path('clue_list/', views.clue_list, name='clue_list'),
    path('add_clue/', views.add_clue, name='add_clue'),
    path('clue/<int:clue_id>/', views.clue_detail, name='clue_detail'),
    path('edit-clue/<int:clue_id>/', views.edit_clue, name='edit_clue'),
    path('opportunities/', views.opportunity_list, name='opportunity_list'),
    path('add_opportunity/', views.add_opportunity, name='add_opportunity'),
    path('opportunity/<int:opportunity_id>/', views.opportunity_detail, name='opportunity_detail'),
    path('edit-opportunity/<int:opportunity_id>/', views.edit_opportunity, name='edit_opportunity'),
    path('send_factor_whatsapp/<int:order_id>/', views.send_factor_whatsapp, name='send_factor_whatsapp'),
    path('order_from_id/', views.create_order_from_id, name='create_order_from_id'),
    path('reportage/', views.ReportageView.as_view(), name='reportage_list'),
    path('order_from_file/', views.create_order_from_file, name='create_order_from_file')
]
