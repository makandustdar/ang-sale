from django.urls import path

from users.views import exhibition_views as views


urlpatterns = [
    path('list/', views.ExhibitionList.as_view(), name='exhibition_list'),
    path('add/', views.add, name="exhibition_add"),
    path('edit/<id>/', views.edit, name="exhibition_edit"),
]
