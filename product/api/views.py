import ast

from django.core.serializers import serialize
from django.db.models.functions import Concat
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Value, F, Sum, Q

from product.models import Color, Product, ProductColor

import json


def cabinets_colors(request):
    cabinets = Color.objects.filter(productcolor__product__engName='cabinet').values('name', 'image', 'colorCode',
                                                                                     'isActive', 'productCode', 'pk')
    serialized_colors_queryset = json.dumps(list(cabinets), cls=DjangoJSONEncoder).encode('utf8').decode(
        'unicode-escape')
    return HttpResponse(serialized_colors_queryset, content_type='application/json')


def high_glass_colors(request):
    high_glasses = Color.objects.filter(productcolor__product__engName='high glass').values('name', 'image',
                                                                                            'colorCode',
                                                                                            'isActive', 'productCode',
                                                                                            'pk')
    serialized_colors_queryset = json.dumps(list(high_glasses), cls=DjangoJSONEncoder).encode('utf8').decode(
        'unicode-escape')
    return HttpResponse(serialized_colors_queryset, content_type='application/json')


def psd_colors(request):
    psd_glasses = Color.objects.filter(productcolor__product__engName='psd').values('name', 'image', 'colorCode',
                                                                                    'isActive', 'productCode', 'pk')
    serialized_colors_queryset = json.dumps(list(psd_glasses), cls=DjangoJSONEncoder).encode('utf8').decode(
        'unicode-escape')
    return HttpResponse(serialized_colors_queryset, content_type='application/json')


def colors_list(request):
    colors_queryset = Color.objects.values('name', 'image', 'colorCode', 'isActive', 'productCode', 'pk')
    serialized_colors_queryset = json.dumps(list(colors_queryset), cls=DjangoJSONEncoder)
    return HttpResponse(serialized_colors_queryset, content_type='application/json')


# def users_list(request):
#     User = get_user_model()
#     # annotate fullname with fname and lname: if profile has private, it'll fill with private's fname and lname
#     # if there is no private then it'll fill with legal's
#     users_queryset = User.objects.annotate(
#         fullname=Concat(F('profile__private__fname'), Value(' '), F('profile__private__lname'),
#                         F('profile__legal__fname'), Value(' '), F('profile__legal__lname'))
#     )
#     users_queryset = users_queryset.values('pk', 'username', 'first_name', 'last_name', 'email', 'fullname')
#     serialized_users_queryset = json.dumps(list(users_queryset), cls=DjangoJSONEncoder)
#
#     return HttpResponse(serialized_users_queryset, content_type='application/json')


def get_colors(request):
    colors_id_string = request.GET.get('colors')
    colors_id = ast.literal_eval(colors_id_string)
    colors = Color.objects.filter(id__in=colors_id).values('name', 'image', 'colorCode', 'isActive', 'productCode',
                                                           'pk')
    serialized_colors_queryset = json.dumps(list(colors), cls=DjangoJSONEncoder).encode('utf8').decode('unicode-escape')
    return HttpResponse(serialized_colors_queryset, content_type='application/json')

# def get_customer(request):
#     customer_id_string = request.GET.get('user')
#     users_id = ast.literal_eval(customer_id_string)
#
#     User = get_user_model()
#     users = User.objects.filter(id__in=users_id)
#     users = users.annotate(
#         fullname=Concat(F('profile__private__fname'), Value(' '), F('profile__private__lname'),
#                         F('profile__legal__fname'), Value(' '), F('profile__legal__lname'))
#     )
#     users_queryset = users.values('pk', 'username', 'first_name', 'last_name', 'email', 'fullname')
#     serialized_users_queryset = json.dumps(list(users_queryset), cls=DjangoJSONEncoder).encode('utf8').decode('unicode-escape')
#     return HttpResponse(serialized_users_queryset, content_type='application/json')
