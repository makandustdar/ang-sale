from django.urls import path
from django.contrib.auth.views import LogoutView

from users.views import admin_views as views


urlpatterns = [
    # path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name="admin_profile"),
    path('login/', views.admin_login, name="admin_login"),
    path('logout/', LogoutView.as_view(template_name="auth/admin/login.html"),
         name='admin_logout'),
    path('change-password/', views.change_password, name='change_password'),
]
