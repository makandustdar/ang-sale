from .models import *
from ippanel import Client


def send_order_notification(user, status, trackName, transId):
    if status == 'REGISTER':
        title = 'ثبت سفارش'
        text = f'سفارش با شماره تراکنش {transId} ثبت شد'
    else:
        title = 'تغییر وضعیت سفارش'
        text = f'سفارش به شماره {transId} به وضعیت \"{trackName}\" تغییر یافت'

    Notification.objects.get_or_create(user=user, title=title, text=text)


def send_confirmation_code(name, code, mobile):
    api_key = 'oV49VQNYQv37gwIQsYjAJp8URE3RgL-z06w2sUfTiEY='
    sms = Client(api_key)
    pattern_values = {
        "name": name,
        "code": code,
    }

    try:
        bulk_id = sms.send_pattern(
            "k58n4blrcu",  # pattern code
            "3000505",  # originator
            mobile,  # recipient
            pattern_values,  # pattern values
        )
        message = sms.get_message(bulk_id)
        return message
    except:
        return False


def send_birthday_sms(name, mobile):
    api_key = 'oV49VQNYQv37gwIQsYjAJp8URE3RgL-z06w2sUfTiEY='
    sms = Client(api_key)
    pattern_values = {
        "name": name,
    }

    try:
        bulk_id = sms.send_pattern(
            "5ca2qa63x97mvpy",  # pattern code
            "3000505",  # originator
            mobile,  # recipient
            pattern_values,  # pattern values
        )
        message = sms.get_message(bulk_id)
        return message
    except Exception as e:
        print(e)
        return False


def send_password_to_expert(mobile, password, username):
    api_key = 'oV49VQNYQv37gwIQsYjAJp8URE3RgL-z06w2sUfTiEY='
    sms = Client(api_key)
    pattern_values = {
        "username": username,
        "password": password,
    }

    bulk_id = sms.send_pattern(
        "dsiwn1or8jlv6yh",  # pattern code
        "3000505",  # originator
        mobile,  # recipient
        pattern_values,  # pattern values
    )


def check_if_orderitem_exists(productId, featureValues, color, order):
    orderitemIds = OrderItem.objects.filter(
        order=order, product_id=productId, color=color).values_list('id', flat=True)

    error_list = []

    if not orderitemIds:
        return False
    else:
        for orderitemId in orderitemIds:
            result = check_if_orderitemdetail_exists(
                orderitemId, featureValues)
            if result > 0:
                return result
            else:
                error_list.append(result)

        if sum(error_list) == 0:
            return False


def check_if_orderitemdetail_exists(orderitemId, featureValues):
    for i in featureValues:
        featureId = i.split('|')[0]
        featureValueId = i.split('|')[1]

        feature = Feature.objects.get(id=featureId)
        featureValue = FeatureValue.objects.get(id=featureValueId)

        q = OrderItemDetail.objects.filter(orderitem_id=orderitemId,
                                           featureName=feature.perName,
                                           featureValueName=featureValue.name)

        if not q.exists():
            return 0

    return orderitemId


def send_order_sms(status, name, mobile, pre_holding_code=None):
    api_key = 'oV49VQNYQv37gwIQsYjAJp8URE3RgL-z06w2sUfTiEY='
    sms = Client(api_key)
    pattern_values = {
        "name": name
    }

    if status == 'REGISTER':
        pattern_code = 'o4ew0y3xcmqt8no'
    elif status == 'HOLDING':
        pattern_code = '4oxi9i1tkyoucl0'
    elif status == 'PRODUCING':
        pattern_code = 'kgcph62wxrypvv8'
    elif status == 'PAYING':
        pattern_code = 'zw2yf0vw1p421ey'
    elif status == 'COMPLETE':
        pattern_code = 'f6zu0tqc6yps0ew'
    elif status == 'PRE_HOLDING':
        pattern_code = 'bbbrrmyz42tjqlo'
        # convert to string (check farazsms config for this pattern)
        pattern_values = {
            "code": str(pre_holding_code)
        }

    try:
        bulk_id = sms.send_pattern(
            pattern_code,  # pattern code
            "3000505",  # originator
            mobile,  # recipient
            pattern_values,  # pattern values
        )
        message = sms.get_message(bulk_id)
        return message
    except Exception as e:
        return False
