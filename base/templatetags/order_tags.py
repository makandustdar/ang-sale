from django import template

register = template.Library()


@register.simple_tag()
def parse_track(track_string):
    if track_string == 'REGISTER':
        return 'ثبت شده'
    elif track_string == 'PRODUCING':
        return 'در حال آماده سازی'
    elif track_string == 'COMPLETE':
        return 'آماده شده'


@register.simple_tag()
def parse_track_class(track_string):
    if track_string == 'REGISTER':
        return 'text-primary'
    elif track_string == 'PRODUCING':
        return 'text-secondary'
    elif track_string == 'COMPLETE':
        return 'text-success'


@register.simple_tag()
def orders_count(profile):
    all_orders = profile.user.user_orders.all()
    registered_orders = all_orders.filter(track='REGISTER')
    producing_orders = all_orders.filter(track='PRODUCING')
    completed_orders = all_orders.filter(track='COMPLETE')
    return {
        "all_orders": all_orders.count(),
        "registered_orders": registered_orders.count(),
        "producing_orders": producing_orders.count(),
        "completed_orders": completed_orders.count(),
    }


@register.simple_tag()
def get_order_item_detail_set_names(items):
    qs = items.values('id')
    output = [item['id'] for item in qs]
    return output


@register.simple_tag()
def parse_price(price):
    return f'{price:,.0f}'
