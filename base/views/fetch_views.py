import ast

from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core import serializers
from django.db.models import Max
from django.shortcuts import get_object_or_404

import json
import random

from base.models import *
from base.utils import *
from users.models import *


@user_passes_test(lambda u: u.is_staff, login_url='/admin/login/')
def feature_add(request):
    data = json.loads(request.body)
    f_name = data['feature_name']

    if Feature.objects.filter(name=f_name).exists():
        message = {'status_code': '400', 'text': 'مشخصه وجود دارد'}
    else:
        Feature.objects.create(name=f_name)
        message = {'status_code': '200', 'text': 'مشخصه ایجاد شد'}

    features = list(Feature.objects.filter(is_active=True).values())
    return JsonResponse({'message': message, 'features': features}, safe=False)


def filter_color(request):
    productId = request.GET.get('productId')
    productName = request.GET.get('productName')
    brands = Feature.objects.get(perName='برند').featurevalues.filter(productfeaturevalue__product__perName='های گلاس')
    colors = ProductColor.objects.filter(product_id=productId)
    t = render_to_string('product/ajax/color-list.html', {'colors': colors, 'product': productName, 'brands': brands},
                         request=request)
    return JsonResponse({'data': t})


def color_image(request):
    colorId = request.GET.get('colorId')
    color = Color.objects.get(id=colorId)
    message = {'color_image': color.image.url}

    return JsonResponse(message, safe=False)


def get_product_features(request):
    productId = request.GET.get('productId')
    product = Product.objects.get(id=productId)

    colors = ProductColor.objects.filter(product=product)

    featurevalues = ProductFeatureValue.objects.filter(product_id=productId).values('featurevalue__feature__id',
                                                                                    'featurevalue__feature__perName',
                                                                                    'featurevalue__id',
                                                                                    'featurevalue__name').order_by(
        'priority')
    user = request.user
    t = render_to_string('order/ajax/features.html',
                         {'featurevalues': featurevalues, 'product': product, 'colors': colors, 'user': user})
    return JsonResponse({'data': t})


@login_required(login_url='users/login/')
def pre_order_edit(request):
    data = json.loads(request.body)
    itemId = data['itemId']
    quantity = data['quantity']
    colorId = data['color']
    fee = data['fee']
    print(fee)
    featureValueIdList = data['featureValueIdList']
    color = None
    if colorId != '':
        color = Color.objects.get(id=colorId)
    for i in featureValueIdList:
        orderitemdetailId = i.split("|")[0]
        featureId = i.split("|")[1]
        featureValueId = i.split("|")[2]

        feature = Feature.objects.get(id=featureId)
        featureValue = FeatureValue.objects.get(id=featureValueId)

        OrderItemDetail.objects.filter(id=orderitemdetailId).update(feature=feature, featureName=feature.perName,
                                                                    featureValue=featureValue,
                                                                    featureValueName=featureValue.name)

        if color:
            OrderItem.objects.filter(id=itemId).update(color=color, colorName=color.name)
        if fee:
            fee = fee.replace(',', '')
            OrderItem.objects.filter(id=itemId).update(fee=fee)
        if quantity:
            OrderItem.objects.filter(id=itemId).update(quantity=quantity)

        message = {'status': 'success', 'text': 'سفارش با موفقیت ویرایش شد'}

    return JsonResponse(message, safe=False)


@login_required(login_url='users/login/')
def pre_order_delete(request):
    data = json.loads(request.body)
    itemId = data['itemId']
    OrderItem.objects.filter(id=itemId).delete()

    message = {'status': 'success', 'text': 'محصول از سبد سفارش حذف شد'}
    return JsonResponse(message, safe=False)


@login_required(login_url='users/login/')
def order_delete(request):
    data = json.loads(request.body)
    itemId = data['itemId']
    Order.objects.filter(id=itemId).delete()

    message = {'status': 'success', 'text': 'سفارش حذف شد!'}
    return JsonResponse(message, safe=False)


@login_required(login_url='users/login/')
def order_update(request):
    data = json.loads(request.body)
    print(data)
    # pass


@login_required(login_url='users/login/')
def order_complete(request):
    data = json.loads(request.body)
    orderId = data['orderId']
    action = data['action']
    trans_id = random.randint(1000000, 9999999)

    order = Order.objects.get(id=orderId)
    order.transId = trans_id
    order.completed = True

    if action == 'cancel':
        order.track = 'CANCEL'
        status = 'success'
        title = 'لغو سفارش'
        text = 'سفارش لغو شد'
    else:
        order.track = 'REGISTER'
        status = 'success'
        title = 'تکمیل سفارش'
        text = 'سفارش باموفقیت ثبت شد'
    order.save()

    # send sms to user
    send_order_sms(order.track, order.user.profile.get_full_name, order.user.profile.mobile)

    # send notification to user
    send_order_notification(order.user, 'REGISTER', None, order.transId)
    message = {'status': status, 'title': title, 'text': text}

    return JsonResponse(message, safe=False)


@user_passes_test(lambda u: u.is_staff, login_url='/admin/login/')
def order_change_status(request):
    data = json.loads(request.body)
    order_id = data['orderId']
    trackValue = data['trackValue']
    track_name = data['trackName']
    send_sms = data['send_sms']
    order = Order.objects.get(id=order_id)
    if trackValue != 'HOLDING':
        order.confirmed = True
        related_code_object = OrderConfirmationCode.objects.filter(order=order).first()
        if related_code_object:
            related_code_object.delete()
    order.track = trackValue
    order.save()

    if send_sms:
        if trackValue == 'HOLDING':
            confirmation_code = random.randint(1000000, 9999999)
            order.confirmed = False
            order.save()
            send_order_sms('PRE_HOLDING', order.user.profile.get_full_name, order.user.profile.mobile,
                           pre_holding_code=confirmation_code)
            OrderConfirmationCode.objects.create(order=order, code=confirmation_code)
        send_order_sms(trackValue, order.user.profile.get_full_name,
                       order.user.profile.mobile)

    # send notification to user
    send_order_notification(order.user, trackValue, track_name, order.transId)
    return JsonResponse({'status': 200, 'waiting': True}, safe=False)


@user_passes_test(lambda u: u.is_staff, login_url='/admin/login/')
def update_status(request):
    data = json.loads(request.body)
    id = data['id']
    status = data['value']
    db = data['db']

    if db == 'users' or db == 'expert':
        q = User.objects.filter(id=id)

    if status:
        q.update(is_active=True)
        message = {'status': 'success', 'text': 'وضعیت فعال شد'}
    else:
        q.update(is_active=False)
        message = {'status': 'success', 'detail': 'وضعیت غیرفعال شد'}

    return JsonResponse(message, safe=False)


@user_passes_test(lambda u: u.is_staff, login_url='/admin/login/')
def featurevalue_edit(request):
    data = json.loads(request.body)
    name = data['name']
    code = data['code']
    id = data['id']
    productId = data['product']

    FeatureValue.objects.filter(id=id).update(name=name, code=code)
    ProductFeatureValue.objects.filter(
        featurevalue_id=id).update(product_id=productId)

    message = {'status': '200', 'text': 'مشخصه محصول ویرایش شد'}
    return JsonResponse(message, safe=False)


def get_city(request):
    state = request.GET.get('state')

    data = serializers.serialize('json', City.objects.filter(state=state))
    return HttpResponse(data, content_type="application/json")


def get_features(request):
    per_feature_names = list(Feature.objects.filter(
        isActive=True).values_list('perName', flat=True))
    eng_feature_names = list(Feature.objects.filter(
        isActive=True).values_list('engName', flat=True))

    return HttpResponse(json.dumps({'per_feature_names': per_feature_names, 'eng_feature_names': eng_feature_names}))


def get_feature_details(request):
    featureName = request.GET.get('featureName')
    productId = request.GET.get('productId')

    feature_details = list(Feature.objects.filter(
        perName=featureName).values_list('engName', flat=True))

    if feature_details:
        feature_details = feature_details[0]
    else:
        feature_details = None

    priority = list(ProductFeatureValue.objects.filter(
        product_id=productId,
        featurevalue__feature__perName=featureName).values_list('priority', flat=True).distinct())

    if priority:
        priority = priority[0]
    else:
        priority = ProductFeatureValue.objects.filter(
            product_id=productId).aggregate(priority=Max('priority'))
        priority = int(priority['priority']) + 1

    return HttpResponse(json.dumps({'engFeatureName': feature_details, 'priority': priority}))


def get_user_info(request):
    userId = request.GET.get('userId')
    if userId:
        profile = Profile.objects.get(user__id=userId)

        if profile.role == 2:
            company = profile.legal.company_name
        else:
            company = ''
        address = profile.state.name + '.' + profile.city.name + '.' + profile.address
        zipcode = profile.zipcode
        mobile = profile.mobile

        return JsonResponse({'company': company, 'address': address,
                             'zipcode': zipcode, 'mobile': mobile}, safe=False)


def notification_read(request):
    data = json.loads(request.body)

    id = data['id']

    if not request.user.is_staff:
        q = Notification.objects.filter(user=request.user)
        if id == 'all':
            q.update(userRead=True)
        else:
            q.filter(id=id).update(userRead=True)
    else:
        q = Notification.objects.all()
        if id == 'all':
            q.update(adminRead=True)
        else:
            q.filter(id=id).update(adminRead=True)

    return JsonResponse('done', safe=False)


def get_color_names(request):
    colors_id = request.GET.get('colors')
    colors_id = ast.literal_eval(colors_id)
    if colors_id:
        colors = Color.objects.filter(id__in=colors_id)
        return JsonResponse(list(colors.values('name', 'id')), safe=False)
    return HttpResponse('None')


def get_cities(request, state_id):
    city_selected = request.GET.get('city_selected', None)
    city = None
    if city_selected != 'undefined':
        city = City.objects.get(name=city_selected)
    state = State.objects.get(id=state_id)
    data = serializers.serialize('json', City.objects.filter(state=state.id))
    list_data = json.loads(data)
    if city_selected != 'undefined' and city:
        selected_city_dict = {
            'selected': city.id
        }
        list_data.append(selected_city_dict)
    data = json.dumps(list_data).encode('utf-8')
    return HttpResponse(data, content_type="application/json")
