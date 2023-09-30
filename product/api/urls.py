from django.urls import path
from .views import colors_list, get_colors, cabinets_colors, high_glass_colors, psd_colors

urlpatterns = [
    path('customer-colors/', get_colors, name='get_colors'),
    path('cabinets-colors/', cabinets_colors, name='cabinets_colors'),
    path('high-glass-colors/', high_glass_colors, name='cabinets_colors'),
    path('psd-colors/', psd_colors, name='cabinets_colors')
]
