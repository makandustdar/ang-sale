from django.contrib import admin
from .models import Feature, ProductFeature, Color, Product, ProductColor, ProductFeatureValue


# Register your models here.

class ProductFeatureAdmin(admin.ModelAdmin):
    list_filter = ['feature']


admin.site.register(Feature)
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(ProductColor)
admin.site.register(ProductFeature, ProductFeatureAdmin)
admin.site.register(ProductFeatureValue)