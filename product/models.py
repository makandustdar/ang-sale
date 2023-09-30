from django.db import models
from .managers import ActivesManager

class Product(models.Model):
    perName = models.CharField(max_length=200)
    engName = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    color = models.ManyToManyField('Color', null=True)
    isActive = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.perName


class Feature(models.Model):
    perName = models.CharField(max_length=200)
    engName = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    visibility = models.BooleanField(default=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.perName


class FeatureValue(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.SET_NULL, null=True, related_name='featurevalues')
    name = models.CharField(max_length=200)
    isActive = models.BooleanField(default=True)
    code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    feature = models.ForeignKey(Feature, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.product.perName


class ProductFeatureValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    featurevalue = models.ForeignKey(
        FeatureValue, on_delete=models.SET_NULL, null=True)
    priority = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.product.perName


class Color(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='colors/', blank=True, null=True)
    colorCode = models.CharField(max_length=10, blank=True, null=True)
    productCode = models.CharField(max_length=10, blank=True, null=True)
    isActive = models.BooleanField(default=True)
    brand = models.CharField(max_length=100, blank=True, null=True)

    objects = models.Manager
    actives = ActivesManager

    def __str__(self):
        return self.name

    @property
    def get_image(self):
        if self.image:
            return self.image
        else:
            return ''


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
