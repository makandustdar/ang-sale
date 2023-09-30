import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from product.models import Product


class ProductList(PermissionRequiredMixin, ListView):
    model = Product
    permission_required = 'product.view_product'
    template_name = "product/list.html"
    context_object_name = 'products'
    paginate_by = 10
    queryset = Product.objects.all().order_by('-createdAt')


@permission_required('product.add_product', login_url='/admin/login/')
def add(request):
    if request.method == 'POST':
        perName = request.POST.get('perName')
        engName = request.POST.get('engName')
        colors = request.POST.getlist('color')

        p, created = Product.objects.get_or_create(perName=perName)
        p.engName = engName
        p.slug = engName.replace(' ', '-')
        p.save()

        if colors:
            for color in colors:
                ProductColor.objects.get_or_create(
                    product=p, color=Color.objects.get(id=color))
        messages.success(request, 'محصول با موفقیت اضافه شد')
        return redirect('feature_list')

    colors = Color.objects.all()
    return render(request, 'product/add.html', {'colors': colors})


@permission_required('product.add_product', login_url='/admin/login/')
def edit(request, productId):
    product = Product.objects.get(id=productId)

    if request.method == 'POST':
        perName = request.POST.get('perName')
        engName = request.POST.get('engName')
        colors = request.POST.getlist('color')
        priority = request.POST.getlist('priority')
        priority.reverse()

        product.perName = perName
        product.engName = engName
        product.slug = engName.replace(' ', '-')
        product.save()

        ProductColor.objects.filter(product=product).delete()
        if colors:
            for color in colors:
                ProductColor.objects.get_or_create(
                    product=product, color=Color.objects.get(id=color))

        for i in range(len(priority)):
            ProductFeatureValue.objects.filter(
                product=product, featurevalue__feature__id=priority[i]).update(priority=i + 1)

        messages.success(request, 'محصول با موفقیت ویرایش شد')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    colors = Color.objects.all()
    features = list(ProductFeatureValue.objects.filter(product=product).values(
        'featurevalue__feature__perName', 'featurevalue__feature__id').order_by('-priority').distinct())

    context = {'product': product, 'colors': colors, 'features': features}
    return render(request, 'product/edit.html', context)


class FeatureList(PermissionRequiredMixin, ListView):
    model = Feature
    template_name = 'product/feature-list.html'
    context_object_name = 'features'
    permission_required = 'product.add_product'


@permission_required('product.add_product', login_url='/admin/login/')
def feature_add(request):
    if request.method == 'POST':
        productId = request.POST.get('product')

        perName = list(eval(request.POST.getlist('perName')[0]))[0]['value']
        engName = list(eval(request.POST.getlist('engName')[0]))[0]['value']

        visibility = request.POST.get('visibility')
        priority = request.POST.get('priority')

        product = Product.objects.get(id=productId)
        feature, created = Feature.objects.get_or_create(perName=perName)

        feature.engName = engName
        feature.slug = engName.replace(' ', '-')
        feature.visibility = visibility
        feature.save()

        for i in range(int((len(request.POST) - 6) / 2)):
            featureValue = request.POST.get(f'group-a[{i}][featureValue]')
            featureValueCode = request.POST.get(
                f'group-a[{i}][featureValueCode]')

            featurevalue, created = FeatureValue.objects.get_or_create(
                feature=feature, name=featureValue, code=featureValueCode)

            productfeaturevalue, created = ProductFeatureValue.objects.get_or_create(
                product=product, featurevalue=featurevalue)
            productfeaturevalue.priority = priority
            productfeaturevalue.save()

        productfeature, created = ProductFeature.objects.get_or_create(
            product=product, feature=feature)
        productfeature.save()

        messages.success(request, 'مشخصه محصول ایجاد شد')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    products = Product.objects.filter(isActive=True).order_by('-createdAt')

    context = {'products': products}
    return render(request, 'product/feature-add.html', context)


@permission_required('product.add_product', login_url='/admin/login/')
def feature_edit(request, featureId):
    feature = Feature.objects.get(id=featureId)

    if request.method == 'POST':
        perName = request.POST.get('perName')
        engName = request.POST.get('engName')
        visibility = request.POST.get('visibility')

        feature.perName = perName
        feature.engName = engName
        feature.slug = engName.replace(' ', '-')
        feature.visibility = visibility

        feature.save()

        messages.success(request, 'مشخصه محصول ویرایش شد')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    products = Product.objects.filter(isActive=True).order_by('-createdAt')

    context = {'feature': feature, 'products': products}
    return render(request, 'product/feature-edit.html', context)


def feature_value_add(request, feature_id):
    if request.method == 'POST':
        code = request.POST.get('featureValueCode')
        name = request.POST.get('featureValueName')
        product_id = request.POST.get('product')
        feature_value = FeatureValue.objects.create(feature_id=feature_id, name=name, code=code)
        product = Product.objects.get(id=product_id)
        feature_value.productfeaturevalue_set.update(product=product)
        feature_value.save()
        ProductFeatureValue.objects.create(product=product, featurevalue=feature_value)
        return redirect(reverse('feature_edit', kwargs={'featureId': feature_id}))


class ColorList(ListView):
    model = Color
    template_name = 'product/color-list.html'
    context_object_name = 'colors'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['highglass_brands'] = Feature.objects.get(perName='برند').featurevalues.filter(
            productfeaturevalue__product__perName='های گلاس')
        context['products'] = Product.objects.filter(isActive=True)
        return context


def color_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        colorCode = request.POST.get('colorCode')
        productCode = request.POST.get('productCode')

        if Color.objects.filter(name=name).exists():
            messages.error(request, 'رنگ قبلا وارد شده است')
        else:
            color = Color.objects.create(
                name=name, colorCode=colorCode, productCode=productCode)
            if image:
                fs = FileSystemStorage()
                filename = fs.save(image.name, image)
                uploaded_file_url = fs.url(filename)
                color.image = uploaded_file_url
                color.save()
            messages.success(request, f'رنگ {name} ایجاد شد')
        return redirect('color_list')


def color_edit(request, colorId):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        brand = request.POST.get('brand')
        colorCode = request.POST.get('colorCode')
        productCode = request.POST.get('productCode')
        status = request.POST.get('status')

        if Color.objects.filter(name=name).exclude(id=colorId).exists():
            messages.error(request, 'رنگ قبلا وارد شده است')
        else:
            color = Color.objects.get(id=colorId)
            color.name = name
            color.brand = brand
            color.colorCode = colorCode
            color.productCode = productCode
            color.isActive = status

            if image:
                fs = FileSystemStorage()
                filename = fs.save(image.name, image)
                uploaded_file_url = fs.url(filename)
                color.image = uploaded_file_url
            color.save()
            messages.success(request, f'رنگ {name} ویرایش شد')
        return redirect('color_list')


def color_delete(request, color_id):
    if request.method == 'POST':
        print(color_id)
        color = Color.objects.get(id=color_id)
        color.delete()
        return redirect('color_list')
