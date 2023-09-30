from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.cache import cache
from django.views.generic import ListView, UpdateView, DeleteView
from django.db.models import Count, Q, Sum, Value, F, FloatField
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin

from datetime import datetime
import jdatetime

from base.models import *
from base.utils import *
from product.models import *
from users.models import *


class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


class OrderList(ListView):
    model = Order
    template_name = "order/list.html"
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        orders = Order.objects.filter(
            completed=True, user=self.request.user).order_by('-createdAt')

        q = self.request.GET.get('q')
        track = self.request.GET.get('track')
        sort = self.request.GET.get('sort')

        if q:
            orders = orders.filter(Q(user__profile__private__fname__icontains=q) |
                                   Q(user__profile__legal__fname__icontains=q) | Q(
                user__profile__private__lname__icontains=q) |
                                   Q(user__profile__legal__lname__icontains=q) | Q(
                user__profile__mobile__contains=q) | Q(transId__contains=q))

        if track:
            orders = orders.filter(track=track)

        if sort:
            if sort == 'asc':
                orders = orders.order_by('createdAt')
            elif sort == 'desc':
                orders = orders.order_by('-createdAt')

        return orders


class AdminOrderList(AdminStaffRequiredMixin, ListView):
    model = Order
    permission_required = 'base.view_order'
    template_name = "order/list.html"
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_superuser:
            orders = Order.objects.filter(
                completed=True).order_by('-createdAt')
        else:
            orders = Order.objects.filter(
                expert=self.request.user.expert, completed=True).order_by('-createdAt')
            print(Order.objects.filter(expert=self.request.user.expert))

        q = self.request.GET.get('q')
        track = self.request.GET.get('track')
        sort = self.request.GET.get('sort')
        year = self.request.GET.get('year')
        if year:
            orders = orders.filter(order_date__year=int(year))

        if q:
            orders = orders.filter(Q(user__profile__private__fname__icontains=q) |
                                   Q(user__profile__legal__fname__icontains=q) | Q(
                user__profile__private__lname__icontains=q) |
                                   Q(user__profile__legal__lname__icontains=q) | Q(
                user__profile__mobile__contains=q) | Q(transId__contains=q))

        if track:
            orders = orders.filter(track=track)

        if sort:
            if sort == 'asc':
                orders = orders.order_by('createdAt')
            elif sort == 'desc':
                orders = orders.order_by('-createdAt')
        return orders


@login_required(login_url='/users/login/')
def add(request):
    if request.method == 'POST':
        productId = request.POST.get('product')
        colorId = request.POST.get('color')
        quantity = request.POST.get('quantity')
        productFeatureValues = request.POST.getlist('productfeaturevalue')

        if not productId:
            messages.error(request, 'محصول را انتخاب کنید')
        elif not productFeatureValues:
            messages.error(request, 'مشخصه محصول را به درستی انتخاب نکرده اید')
        elif not quantity:
            messages.error(request, 'فیلد تعداد ضروری میباشد')
        else:
            order, created = Order.objects.get_or_create(
                user=request.user, completed=False, expert=request.user.expert)

            product = Product.objects.get(id=productId)

            code = ''
            if colorId:
                color = Color.objects.get(id=colorId)
                if color.productCode:
                    code += color.productCode
                colorName = color.name
            else:
                color = None
                colorName = None

            exists = check_if_orderitem_exists(productId, productFeatureValues, color)

            if exists:
                orderitem = OrderItem.objects.get(id=exists)
                orderitem.quantity = orderitem.quantity + int(quantity)
                orderitem.save()
            else:
                orderitem = OrderItem.objects.create(order=order, product_id=productId, productName=product.perName,
                                                     quantity=quantity, color=color, colorName=colorName)
                for i in productFeatureValues:
                    featureId = i.split('|')[0]
                    featureValueId = i.split('|')[1]

                    feature = Feature.objects.get(id=featureId)
                    featureValue = FeatureValue.objects.get(id=featureValueId)
                    if featureValue.code:
                        code += featureValue.code

                    OrderItemDetail.objects.create(orderitem=orderitem, feature=feature,
                                                   featureName=feature.perName, featureValue=featureValue,
                                                   featureValueName=featureValue.name)

                orderitem.code = code
                orderitem.save()
            messages.success(request, 'سفارش ثبت شد')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    print('here')
    products = Product.objects.filter(isActive=True).order_by('-createdAt')
    order = Order.objects.filter(completed=False).last()
    items = OrderItem.objects.filter(order=order).order_by('id')
    context = {'products': products, 'order': order, 'items': items}
    return render(request, 'order/add.html', context)


@login_required(login_url='/users/login/')
def submit_order(request):
    if request.method == 'POST':
        order_detail = cache.get('order_detail')
        if not order_detail:
            messages.error(request, 'جهت ثبت سفارش ابتدا روی اعمال کلیک کنید سپس روی تکمیل سفارش کلیک کنید')
            return redirect('set_order_price')
        cache.delete('order_detail')
        payment_type = request.POST.get('payment_type')
        order_description = request.POST.get('orderdescription')

        final_price = order_detail['final_price'].replace(',', '')
        order_items = order_detail['items']
        last_order_trans_id = Order.objects.last().id
        order = order_detail['order']
        order.track = 'REGISTER'
        order.completed = True
        order.price = final_price
        order.description = order_description
        # order.transId = last_order_trans_id + 1
        if payment_type == 'check':
            one_month = request.POST.get('one_month')
            two_month = request.POST.get('two_month')
            three_month = request.POST.get('three_month')
            if one_month:
                order.payment_type = 'CH1'
            elif two_month:
                order.payment_type = 'CH2'
            elif three_month:
                order.payment_type = 'CH3'

        elif payment_type == 'cash':
            order.payment_type = 'CA'
        else:
            messages.error(request, 'نوع پرداخت را انتخاب کنید')
            return redirect('set_order_price')
        order.order_items.set(order_items)
        order.save()
        return redirect('admin_order_list')


@permission_required('base.add_order', login_url='/admin/login/')
def admin_add(request):
    if request.method == 'POST':
        productId = request.POST.get('product')
        colorId = request.POST.get('color')
        creation_date = request.POST.get('creation_date')
        # TODO assign creation date to order or order item
        customer = request.POST.get('customer')
        quantity = request.POST.get('quantity')
        fee_price = request.POST.get('feeprice')
        trans_id = request.POST.get('transId')

        if not trans_id:
            messages.error(request, 'شماره صورت حساب وارد نشده است')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if not creation_date or creation_date == '-':
            messages.error(request, 'تاریخ صدور وارد نشده است')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        productFeatureValues = request.POST.getlist('productfeaturevalue')
        if not productId:
            messages.error(request, 'محصول را انتخاب کنید')
        elif not productFeatureValues:
            messages.error(request, 'مشخصه محصول را به درستی انتخاب نکرده اید')

        elif not quantity:
            messages.error(request, 'فیلد تعداد ضروری میباشد')

        else:
            order, created = Order.objects.get_or_create(user_id=customer, completed=False, expert=request.user.expert)
            product = Product.objects.get(id=productId)
            if trans_id:
                order.transId = trans_id
            if creation_date != '-' and creation_date is not None:
                date_time_obj = datetime.strptime(creation_date, '%Y-%m-%d')
                date_time_obj = jdatetime.date(date_time_obj.year, date_time_obj.month, date_time_obj.day,
                                               locale='fa_IR').togregorian()
                jalalidate = jdatetime.date.fromgregorian(year=date_time_obj.year, month=date_time_obj.month,
                                                          day=date_time_obj.day)
                date_time_obj = datetime(jalalidate.year, jalalidate.month, jalalidate.day)
                order.order_date = date_time_obj
            order.save()

            code = ''
            if colorId:
                color = Color.objects.get(id=colorId)
                if color.productCode:
                    code += color.productCode
                colorName = color.name
            else:
                color = None
                colorName = None

            exists = check_if_orderitem_exists(
                productId, productFeatureValues, color, order)

            fee_price = fee_price.replace(',', '')
            order_item = OrderItem.objects.create(order=order, product_id=productId, productName=product.perName,
                                                  quantity=quantity, color=color, colorName=colorName,
                                                  fee=fee_price)
            for i in productFeatureValues:
                featureId = i.split('|')[0]
                featureValueId = i.split('|')[1]
                feature = Feature.objects.get(id=featureId)
                featureValue = FeatureValue.objects.get(id=featureValueId)
                if featureValue.code:
                    code += featureValue.code

                OrderItemDetail.objects.create(orderitem=order_item, feature=feature,
                                               featureName=feature.perName, featureValue=featureValue,
                                               featureValueName=featureValue.name)

            order_item.code = code
            order_item.save()
            messages.success(request, 'سفارش ثبت شد')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    products = Product.objects.filter(isActive=True).order_by('-createdAt')
    users = User.objects.all()
    if request.user.is_superuser:
        pass
    else:
        users = users.filter(
            is_active=True, is_staff=False, profile__expert=request.user.expert).order_by('-date_joined')

    order = Order.objects.filter(completed=False, expert=request.user.expert).last()
    items = OrderItem.objects.filter(order=order).order_by('id')
    context = {'products': products, 'users': users,
               'order': order, 'items': items}
    return render(request, 'order/admin/add.html', context)


@permission_required('base.add_order', login_url='/admin/login/')
def edit(request, orderId):
    order = Order.objects.get(id=orderId)
    if request.method == 'POST':
        customer = request.POST.get('customer')
        transId = request.POST.get('transId')
        order_date = request.POST.get('order_date')
        # year = int(order_date.split('-')[0])
        # month = int(order_date.split('-')[1])
        # day = int(order_date.split('-')[2])
        # date = jdatetime.date(year, month, day)

        # date = jdatetime.date(year, month, day).togregorian()
        # print(date)
        if Order.objects.filter(transId=transId).exclude(id=orderId).exists():
            messages.error(request, 'سفارش با این شماره تراکنش وجود دارد')
        else:
            order.user_id = customer
            order.transId = transId
            order.order_date = order_date
            order.save()

            messages.success(request, 'سفارش باموفقیت ویرایش شد')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    items = OrderItem.objects.filter(order=order).order_by('id')
    users = User.objects.filter(
        is_superuser=False, expert__id=None).order_by('-date_joined')
    products = Product.objects.filter(isActive=True)

    context = {'order': order, 'items': items,
               'users': users, 'products': products}
    return render(request, 'order/edit.html', context)


@login_required(login_url='/users/login/')
def detail(request, order_id):
    order = Order.objects.get(id=order_id)
    items = OrderItem.objects.filter(order=order).order_by('id')
    context = {'order': order, 'items': items}
    return render(request, 'order/detail.html', context)


@login_required(login_url='/users/login/')
def check_confirmation_is_ok(request, order_id):
    order = Order.objects.get(id=order_id)
    confirmation_object = OrderConfirmationCode.objects.get(order=order)
    code = request.POST.get('confirmation_code', None)
    if code:
        if confirmation_object.code == code:
            messages.success(request, 'کد صحیح است')
            confirmation_object.delete()
            order.track = 'PRODUCING'
            order.confirmed = True
            order.save()
            return redirect(reverse('order_detail', kwargs={'order_id': order.id}))
        else:
            messages.error(request, 'کد وارد شده اشتباه است')
            return redirect(reverse('order_detail', args=[order.id]))


@login_required(login_url='/users/login/')
def invoice(request, order_id):
    order = Order.objects.get(id=order_id)
    items = OrderItem.objects.filter(order=order).order_by('id')
    context = {'order': order, 'items': items}
    return render(request, 'order/invoice.html', context)


def update_fee_or_quantity(request, item_id):
    order_item = OrderItem.objects.get(id=item_id)
    fee = request.POST.get("fee")
    quantity = request.POST.get("quantity")
    print(fee)
    fee = fee.replace(',', '')
    print(fee)
    order_item.fee = fee
    order_item.quantity = quantity
    order_item.save()
    messages.success(request, 'آیتم سفارش آپدیت شد')
    return redirect('admin_order_add')


def set_order_price(request):
    order = Order.objects.filter(completed=False).last()
    customer = order.user
    items = OrderItem.objects.filter(order=order).order_by('id')
    # calculate each item's price
    items = items.annotate(price=Sum(F('fee') * F('quantity'), output_field=FloatField()))
    # calculate sum of items prices
    price_aggregated = items.aggregate(total_price=Sum('price'))
    quantity_aggregated = items.aggregate(quantity_sum=Sum('quantity'))

    order_quantity = quantity_aggregated.get('quantity_sum', 0)
    order_price = price_aggregated['total_price']
    if request.method == 'POST':
        off_percent = request.POST.get('off_percent')
        price_percent = request.POST.get('price_percent')
        off_price = request.POST.get('off_price')
        price_price = request.POST.get('price_price')
        includes_tax = True if request.POST.get('tax_checkbox') == 'on' else False
        discount_price = 0
        increase_price_by = 0
        tax = 0
        final_price = order_price

        if includes_tax:
            tax = ((final_price * 9) / 100)
            final_price = final_price + tax
        if off_percent:
            discount_price = (float(off_percent) * float(order_price)) / 100
            final_price = final_price - discount_price

        if price_percent:
            increase_price_by += (float(price_percent) * float(order_price)) / 100
            final_price = final_price + increase_price_by

        if off_price:
            final_price = float(final_price) - float(off_price)

        if price_price:
            increase_price_by += float(price_price)
            final_price = float(final_price) + float(price_price)

        context = {
            'items': items,
            'customer': customer,
            'total_price': f'{order_price:,.0f}',
            'order_quantity': order_quantity,
            'discount_price': f'{discount_price:,.0f}',
            'increase_price_by': f'{increase_price_by:,.0f}',
            'tax': f'{tax:,.0f}',
            'final_price': f'{final_price:,.0f}',
            'off_percent': off_percent,
            'price_percent': price_percent,
            'off_price': off_price,
            'price_price': price_price,
            'order': order
        }
        cache.set('order_detail', context)

    else:
        context = {
            'items': items,
            'customer': customer,
            'total_price': f'{order_price:,.0f}',
            'order_quantity': order_quantity,
            'order': order
        }

    return render(request, 'order/admin/price.html', context)


def change_items_price(request):
    item_id = request.POST.get('item_id')
    change_type = request.POST.get('changepricetype')
    amount = request.POST.get('amount')
    item = OrderItem.objects.get(id=item_id)

    if change_type == "OA":
        item.fee -= int(amount) / item.quantity
    if change_type == "OP":
        off_items = item.fee * int(amount) / 100
        item.fee -= off_items
    if change_type == "IA":
        item.fee += int(amount) / item.quantity
    if change_type == "IP":
        off_items = item.fee * int(amount) / 100
        item.fee += off_items

    item.save()
    return redirect('set_order_price')


class OrderDeleteAdminView(AdminStaffRequiredMixin, DeleteView):
    model = Order
    success_url = 'admin_order_list'
