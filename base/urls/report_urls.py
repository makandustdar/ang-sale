from django.urls import path

from base.views import report_views as views

urlpatterns = [
    path('list/', views.ReportList.as_view(), name='report_list'),
    path('add/<order_id>/', views.report_add, name="report_add"),
    path('detail/<report_id>/', views.report_detail, name='report_detail'),

]
