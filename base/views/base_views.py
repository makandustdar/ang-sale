import datetime
import json
from collections import Counter
import random

import jdatetime
import pytz
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Value, Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
# from django.views import View
from django.views.generic import DetailView, ListView, View, TemplateView
# from django.contrib.auth.forms import UserChangeForm
from base.models import Order, Clue, SellOpportunity, OrderItemDetail, OrderItem
from product.models import Product, Feature, FeatureValue, Color
from users.forms import PrivateEditForm, LegalEditForm
from users.models import Profile, State, City, Private
from ..forms import ClueForm, OpportunityForm


class ProfileDetailView(UserPassesTestMixin, DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'base/profile.html'

    def test_func(self):
        profile = self.get_object()
        current_user = self.request.user
        is_owner = current_user == profile.user
        is_superuser = current_user.is_superuser
        is_owner_of_profile_or_superuser = is_owner or is_superuser
        return is_owner_of_profile_or_superuser

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data()
        profile = self.get_object()
        year = self.request.GET.get('year')
        orders = Order.objects.filter(user__profile=profile)
        if year:
            orders = orders.filter(order_date__year=year)
        if self.request.user.is_staff:
            expert_orders = Order.objects.filter(expert__user=profile.user)
            context['expert_orders'] = expert_orders

        states = State.objects.all()
        cities = City.objects.all()
        context['cities'] = cities
        context['states'] = states
        if profile.role == '1':
            private = Private.objects.get(profile=profile)
            context['user_change_form'] = PrivateEditForm(instance=private)
        if profile.role == '2':
            legal = Private.objects.get(profile=profile)
            context['user_change_form'] = LegalEditForm(instance=legal)
        context['orders'] = orders
        colors_list = []
        products_quantity = []
        total_price = 0
        if 'analysis' in self.request.GET:
            months_annotated = orders.annotate(month=TruncMonth('order_date')).values('order_date__month').annotate(
                total=Count('id'))
            months_vol = list(months_annotated.values_list('order_date__month', 'total'))
            months_dict = dict(months_vol)
            for month in range(1, 13):
                if month not in months_dict.keys():
                    months_dict[month] = 0
            sorted_month_dict = dict(sorted(months_dict.items()))
            sorted_month_dict = json.dumps(sorted_month_dict)
            products_price_dict = {}
            for order in orders:
                product = self.request.GET.get('product')
                for i in order.order_items.all():
                    result = i.fee * i.quantity
                    if i.productName in products_price_dict:
                        products_price_dict[i.productName] += result
                    else:
                        products_price_dict[i.productName] = result
                if product:
                    colors_list.append(
                        list(order.order_items.filter(product__engName=product).values_list('colorName', flat=True)))
                    products_quantity.append(list(
                        order.order_items.filter(product__engName=product).values_list('quantity', 'product__perName')))
                else:
                    colors_list.append(list(order.order_items.all().values_list('colorName', flat=True)))
                    products_quantity.append(list(order.order_items.all().values_list('quantity', 'product__perName')))
                total_price += order.price
            flat_list_colors = [item for sublist in colors_list for item in sublist if item != None]
            flat_list_quantity = [item for sublist in products_quantity for item in sublist if item != None]
            quantity_dict = {}
            for item in flat_list_quantity:
                if item[1] not in quantity_dict.keys():
                    quantity_dict[item[1]] = item[0]
                else:
                    quantity_dict[item[1]] += item[0]
            colors_dict = Counter(flat_list_colors)
            most_common_colors = colors_dict.most_common(3)
            most_common_colors = dict(most_common_colors)
            context['quantity_products'] = quantity_dict
            context['popular_colors'] = most_common_colors
            context['months_volume'] = sorted_month_dict
            context['total_price'] = f'{total_price:,}'
            for key in products_price_dict:
                products_price_dict[key] = f'{products_price_dict[key]:,}'
            context['products_price'] = products_price_dict
        return context


def index(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard_admin')
        else:
            return redirect('dashboard_user')
    else:
        return redirect('login')


@user_passes_test(lambda u: u.is_staff, login_url='/admin/login/')
def dashboard_admin(request):
    users = User.objects.filter(is_staff=False, profile__expert=request.user.profile.expert).count()
    if request.user.is_superuser:
        users = User.objects.filter(is_staff=False).count()
    if request.user.is_superuser:
        orders = Order.objects.filter(completed=True, order_date__year=1402).order_by('-createdAt')
    else:
        orders = Order.objects.filter(
            user__profile__expert=request.user.expert)
    context = {'users': users, 'orders': orders}
    return render(request, 'dashboard_admin.html', context)


@login_required(login_url='/users/login/')
def dashboard_user(request):
    orders = Order.objects.filter(
        user=request.user).order_by('-createdAt')

    context = {'orders': orders}
    return render(request, 'dashboard_user.html', context)


def error_404_view(request):
    # we add the path to the the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')


def clue_list(request):
    clues = Clue.objects.all()
    context = {
        'clues': clues
    }
    return render(request, 'base/clue_list.html', context)


def add_clue(request):
    if request.method == 'POST':
        form = ClueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'سرنخ جدید ثبت شد')
            return redirect('clue_list')
    form = ClueForm()
    context = {
        'form': form
    }
    return render(request, 'base/clue_add.html', context)


def clue_detail(request, clue_id):
    clue = Clue.objects.get(id=clue_id)
    context = {
        'clue': clue
    }
    return render(request, 'base/clue_detail.html', context)


def edit_clue(request, clue_id):
    clue = Clue.objects.get(id=clue_id)
    if request.method == 'POST':
        form = ClueForm(request.POST, instance=clue)
        if form.is_valid():
            form.save()
            messages.success(request, 'سرنخ با موفقیت ویرایش شد')
            return redirect(reverse('clue_detail', kwargs={'clue_id': clue.id}))
    elif request.method == 'GET':
        form = ClueForm(instance=clue)
        context = {
            'form': form
        }
        return render(request, 'base/edit_clue.html', context)


def opportunity_list(request):
    opportunities = SellOpportunity.objects.all()
    context = {
        'opportunities': opportunities
    }
    return render(request, 'base/opportunities_list.html', context)


def add_opportunity(request):
    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'فرصت جدید ثبت شد')
            return redirect('opportunity_list')
    form = OpportunityForm()
    context = {
        'form': form
    }
    return render(request, 'base/opportunity_add.html', context)


def opportunity_detail(request, opportunity_id):
    opportunity = SellOpportunity.objects.get(id=opportunity_id)
    context = {
        'opportunity': opportunity
    }
    return render(request, 'base/opportunity_detail.html', context)


def edit_opportunity(request, opportunity_id):
    opportunity = SellOpportunity.objects.get(id=opportunity_id)
    if request.method == 'POST':
        form = OpportunityForm(request.POST, instance=opportunity)
        if form.is_valid():
            form.save()
            messages.success(request, 'فرصت با موفقیت ویرایش شد')
            return redirect(reverse('opportunity_detail', kwargs={'opportunity_id': opportunity.id}))
    elif request.method == 'GET':
        form = OpportunityForm(instance=opportunity)
        context = {
            'form': form
        }
        return render(request, 'base/edit_opportunity.html', context)


def send_factor_whatsapp(request, order_id):
    order = Order.objects.get(id=order_id)


from io import BytesIO


def create_order_from_file(request):
    if request.method == 'POST':
        upload = request.FILES.get('upload')
        customer = request.POST.get('customer')

        if upload:
            # customer = User.objects.get(id=customer_id)
            full_file = upload.read().decode('utf-16')
            lines_with_no_newlines: list = []
            for line in full_file.split('\n'):
                lines_with_no_newlines.append(line.replace("\n", ""))
            lines_with_no_empty_str: list = [x for x in lines_with_no_newlines if x]
            title_line: int = 0
            first_output: dict = {}
            order_to_create: dict = {}
            orders_index: int = 0
            for idx, line in enumerate(lines_with_no_empty_str):
                line = line.replace('شاخه', '---').replace('\u200f', '').replace('\r', '').replace('","', '||').replace(
                    '%,"', '||').replace('"', '')

                # if 'كالا/خدمت' in line and title_line != idx:
                #     print(line)
                #     title_line = idx
                #     orders_index += 1
                #     first_output: dict = {}
                split_line = line.split(',---,')
                # if len(splx) == 2:
                #     print()
                #     print()
                #     print()
                # split_line = line.split('---')
                if len(split_line) == 2:
                    factor_number = split_line[1].split(',')[-2]
                    if factor_number.isnumeric():
                        split_line = line.split('---')
                        try:
                            fee = split_line[0].split('||')[2]
                        except IndexError:
                            fee = '0'
                        try:
                            quantity = split_line[1].split(',')[1]
                        except IndexError:
                            quantity = '0'

                        if factor_number in first_output.keys():
                            first_output[factor_number].append([fee, quantity])
                        else:
                            first_output[factor_number] = [[fee, quantity]]
                            order_to_create[orders_index] = first_output
                # print(order_to_create)
            order, created = Order.objects.get_or_create(user_id=customer, completed=False,
                                                         expert=request.user.expert)
            for outer_key, outer_values in order_to_create.items():
                for key, value in outer_values.items():
                    print(value)
                    for item in value:
                        fee = int(item[0].replace(',', ''))
                        quantity = int(item[1])
                        if len(key) == 110:
                            product = Product.objects.get(perName='صفحه کابینت')
                            sheet_type_code = key[:2]
                            sheet_width_code = key[2:4]
                            sheets_count_code = key[4:5]
                            color_code = key[6:8]
                            thickness_code = key[-3:-1]
                            hpl_type_code = key[-1]
                            color = Color.objects.filter(productCode=color_code).first()
                            sheet_type = FeatureValue.objects.get(code=sheet_type_code, feature__engName='type')
                            sheet_width = FeatureValue.objects.get(code=sheet_width_code, feature__engName='width')
                            sheets_count = FeatureValue.objects.get(code=sheets_count_code, feature__engName='edge')
                            sheet_thickness = FeatureValue.objects.get(code=thickness_code,
                                                                       feature__engName='thickness')
                            sheet_hpl_type = FeatureValue.objects.get(code=hpl_type_code, feature__engName='HPL Type')
                            features = [sheet_type,
                                        sheet_width,
                                        sheets_count,
                                        sheet_thickness,
                                        sheet_hpl_type]
                        elif (len(key) == 100 and key.startswith('16')) or (
                                len(key) == 90 and key.startswith('16')):
                            product = Product.objects.get(perName='های گلاس')
                            thickness_code = key[:2]
                            brand_code = key[2:-4]
                            color_code = key[-4:]
                            color = Color.objects.get(productCode=color_code)
                            sheet_thickness = FeatureValue.objects.get(code=thickness_code,
                                                                       feature__engName='thickness')
                            sheet_brand = FeatureValue.objects.get(code=brand_code, feature__engName='brand')
                            features = [sheet_brand,
                                        sheet_thickness]

                        elif len(key) == 90 and not key.startswith('16'):
                            product = Product.objects.get(perName='PSD')
                            length_code = key[2:4]
                            quality_code = key[4:5]
                            color_code = key[5:]
                            length = FeatureValue.objects.get(code=length_code, feature__engName='length')
                            quality = FeatureValue.objects.get(code=quality_code, feature__engName='quality')
                            color = Color.objects.get(productCode=color_code)
                            features = [length,
                                        quality]

                        elif len(key) == 80:
                            product = Product.objects.get(perName='فوم PVC')
                            type_code = key[:2]
                            length_code = key[2:4]
                            quality_code = key[4:6]
                            thickness_code2 = key[-2:]
                            sheet_thickness1 = FeatureValue.objects.get(code=type_code, feature__engName='thickness2')
                            sheet_length = FeatureValue.objects.get(code=length_code, feature__engName='length')
                            sheets_quality = FeatureValue.objects.get(code=quality_code, feature__engName='quality')
                            sheet_thickness2 = FeatureValue.objects.get(code=thickness_code2,
                                                                        feature__engName='thickness')

                            features = [sheet_thickness1,
                                        sheet_length,
                                        sheets_quality,
                                        sheet_thickness2]
                        order_item = OrderItem.objects.create(order=order, order_id=order.id, product_id=product.id,
                                                              productName=product.perName)
                        for feature_item in features:
                            feature_id = feature_item.feature_id
                            feature = Feature.objects.get(id=feature_id)
                            inner_order_item = OrderItemDetail.objects.create(orderitem=order_item,
                                                                              feature=feature,
                                                                              featureName=feature.perName,
                                                                              featureValue=feature_item,
                                                                              featureValueName=feature_item.name)

                            inner_order_item.orderitem.color = color
                            inner_order_item.orderitem.colorName = color.name
                            inner_order_item.orderitem.fee = fee
                            inner_order_item.orderitem.quantity = quantity
                            inner_order_item.orderitem.save()
            return redirect('set_order_price')
    elif request.method == 'GET':
        users = User.objects.all()
        return render(request, 'base/order_from_file.html', {'users': users})


def create_order_from_id(request):
    if request.method == 'POST':
        order_raw_id = request.POST.get('order_raw_id')
        customer = request.POST.get('customer')
        color = None
        if len(order_raw_id) == 110:
            product = Product.objects.get(perName='صفحه کابینت')
            sheet_type_code = order_raw_id[:2]
            sheet_width_code = order_raw_id[2:4]
            sheets_count_code = order_raw_id[4:5]
            color_code = order_raw_id[6:8]
            thickness_code = order_raw_id[-3:-1]
            hpl_type_code = order_raw_id[-1]
            color = Color.objects.get(productCode=color_code)
            sheet_type = FeatureValue.objects.get(code=sheet_type_code, feature__engName='type')
            sheet_width = FeatureValue.objects.get(code=sheet_width_code, feature__engName='width')
            sheets_count = FeatureValue.objects.get(code=sheets_count_code, feature__engName='edge')
            sheet_thickness = FeatureValue.objects.get(code=thickness_code, feature__engName='thickness')
            sheet_hpl_type = FeatureValue.objects.get(code=hpl_type_code, feature__engName='HPL Type')
            features = [sheet_type,
                        sheet_width,
                        sheets_count,
                        sheet_thickness,
                        sheet_hpl_type]
        elif (len(order_raw_id) == 100 and order_raw_id.startswith('16')) or (
                len(order_raw_id) == 90 and order_raw_id.startswith('16')):
            product = Product.objects.get(perName='های گلاس')
            thickness_code = order_raw_id[:2]
            brand_code = order_raw_id[2:-4]
            color_code = order_raw_id[-4:]
            color = Color.objects.get(productCode=color_code)
            sheet_thickness = FeatureValue.objects.get(code=thickness_code, feature__engName='thickness')
            sheet_brand = FeatureValue.objects.get(code=brand_code, feature__engName='brand')
            features = [sheet_brand,
                        sheet_thickness]

        elif len(order_raw_id) == 90 and not order_raw_id.startswith('169'):
            product = Product.objects.get(perName='PSD')
            length_code = order_raw_id[2:4]
            quality_code = order_raw_id[4:5]
            color_code = order_raw_id[5:]
            length = FeatureValue.objects.get(code=length_code, feature__engName='length')
            quality = FeatureValue.objects.get(code=quality_code, feature__engName='quality')
            color = Color.objects.get(productCode=color_code)
            features = [length,
                        quality]

        elif len(order_raw_id) == 80:
            product = Product.objects.get(perName='فوم PVC')
            type_code = order_raw_id[:2]
            length_code = order_raw_id[2:4]
            quality_code = order_raw_id[4:6]
            thickness_code2 = order_raw_id[-2:]
            sheet_thickness1 = FeatureValue.objects.get(code=type_code, feature__engName='thickness2')
            sheet_length = FeatureValue.objects.get(code=length_code, feature__engName='length')
            sheets_quality = FeatureValue.objects.get(code=quality_code, feature__engName='quality')
            sheet_thickness2 = FeatureValue.objects.get(code=thickness_code2, feature__engName='thickness')

            features = [sheet_thickness1,
                        sheet_length,
                        sheets_quality,
                        sheet_thickness2]

        order, created = Order.objects.get_or_create(user_id=customer, completed=False, expert=request.user.expert)

        order_item = OrderItem.objects.create(order=order, order_id=order.id, product_id=product.id,
                                              productName=product.perName)
        for feature_item in features:
            feature_id = feature_item.feature_id
            feature = Feature.objects.get(id=feature_id)
            inner_order_item = OrderItemDetail.objects.create(orderitem=order_item,
                                                              feature=feature,
                                                              featureName=feature.perName,
                                                              featureValue=feature_item,
                                                              featureValueName=feature_item.name)

            inner_order_item.orderitem.color = color if color else None
            inner_order_item.orderitem.colorName = color.name if color else None
            inner_order_item.orderitem.save()
        messages.success(request, 'آیتم سفارش ساخته شد')
        return redirect('admin_order_add')


class ReportageView(TemplateView):
    template_name = 'base/reportage.html'

    def get_context_data(self, **kwargs):
        chars = '0123456789ABCDEF'
        random.seed(25)
        context = super().get_context_data()
        year = self.request.GET.get('year')
        month = self.request.GET.get('month')
        now = jdatetime.datetime.now()
        one_month_ago = datetime.datetime(now.year, now.month, 1)
        month_end = datetime.datetime(now.year, now.month + 1, 1) - datetime.timedelta(seconds=1)
        if year and month:
            one_month_ago = datetime.datetime(int(year), int(month), 1)
            try:
                month_end = datetime.datetime(int(year), int(month) + 1, 1) - datetime.timedelta(seconds=1)
            except ValueError as e:
                month_end = datetime.datetime(int(year) + 1, 1, 1) - datetime.timedelta(seconds=1)

        elif month:
            one_month_ago = datetime.datetime(int(now.year), int(month), 1)
            try:
                month_end = datetime.datetime(int(now.year), int(month) + 1, 1) - datetime.timedelta(seconds=1)
            except ValueError as e:
                month_end = datetime.datetime(int(now.year) + 1, 1, 1) - datetime.timedelta(seconds=1)
        orders = Order.objects.filter(order_date__gte=one_month_ago,
                                      order_date__lte=month_end)
        # print(orders.filter(user_id=52).values())
        colors_list = []
        products_quantity = []
        total_price = 0
        months_annotated = orders.annotate(month=TruncMonth('order_date')).values('order_date__month').annotate(
            total=Count('id'))
        months_vol = list(months_annotated.values_list('order_date__month', 'total'))
        months_dict = dict(months_vol)
        for month in range(1, 13):
            if None in months_dict.keys():
                months_dict[0] = months_dict[None]
                del months_dict[None]
            if month not in months_dict.keys():
                months_dict[month] = 0
        sorted_month_dict = dict(sorted(months_dict.items()))
        sorted_month_dict = json.dumps(sorted_month_dict)

        products_price_dict = {}
        cities_sell_dict = {}
        users_dict = {}
        users_dict_price = {}
        payment_type = {}
        for order in orders:
            if order.payment_type in payment_type.keys():
                payment_type[order.payment_type] += 1
            else:
                payment_type[order.payment_type] = 1

            product = self.request.GET.get('product')
            for i in order.order_items.all():
                result = i.fee * i.quantity
                try:
                    if i.order.user.profile.get_full_name in users_dict.keys():
                        try:
                            users_dict_price[i.order.user.profile.get_full_name] += i.fee * i.quantity
                            users_dict[i.order.user.profile.get_full_name] += i.quantity
                        except ObjectDoesNotExist as e:
                            users_dict_price[
                                i.order.user.profile.legal.fname + i.order.user.profile.legal.lname] += i.fee * i.quantity
                            users_dict[
                                i.order.user.profile.legal.fname + i.order.user.profile.legal.lname] += i.quantity
                    else:
                        try:
                            users_dict_price[i.order.user.profile.get_full_name] = i.fee * i.quantity
                            users_dict[i.order.user.profile.get_full_name] = i.quantity
                        except ObjectDoesNotExist as e:
                            users_dict_price[
                                i.order.user.profile.legal.fname + i.order.user.profile.legal.lname] = i.fee * i.quantity
                            users_dict[
                                i.order.user.profile.legal.fname + i.order.user.profile.legal.lname] = i.quantity
                except Exception as e:
                    pass

                if i.productName in products_price_dict:
                    products_price_dict[i.productName] += result
                else:
                    products_price_dict[i.productName] = result

                if i.order.user.profile.city in cities_sell_dict:
                    cities_sell_dict[i.order.user.profile.city] += i.quantity
                else:
                    cities_sell_dict[i.order.user.profile.city.name] = i.quantity
            if product:
                colors_list.append(
                    list(order.order_items.filter(product__engName=product).values_list('colorName', flat=True)))
                products_quantity.append(list(
                    order.order_items.filter(product_id=product).values_list('quantity', 'product__perName')))
            else:
                colors_list.append(list(order.order_items.all().values_list('colorName', flat=True)))
                products_quantity.append(list(order.order_items.all().values_list('quantity', 'product__perName')))
            total_price += order.price
        payment_type2 = {}
        for k, v in payment_type.items():
            if k == 'CH1':
                payment_type2['چک یک ماهه'] = payment_type['CH1']
            elif k == 'CH2':
                payment_type2['چک دو ماهه'] = payment_type['CH2']
            elif k == 'CH3':
                payment_type2['چک سه ماهه'] = payment_type['CH3']
            elif k == 'CA':
                payment_type2['نقد'] = payment_type['CA']
        try:
            del payment_type['CA']
            del payment_type['CH1']
            del payment_type['CH2']
            del payment_type['CH3']
        except KeyError:
            pass
        # try:
        #     payment_type['نقد'] = payment_type['CA']
        #     del payment_type['CA']
        #     payment_type['چک یک ماهه'] = payment_type['CH1']
        #     del payment_type['CH1']
        #     payment_type['چک دو ماهه'] = payment_type['CH2']
        #     del payment_type['CH2']
        #     payment_type['چک سه ماهه'] = payment_type['CH3']
        #     del payment_type['CH3']
        # except KeyError:
        #     pass
        flat_list_colors = [item for sublist in colors_list for item in sublist if item != None]
        flat_list_quantity = [item for sublist in products_quantity for item in sublist if item != None]
        quantity_dict = {}
        for item in flat_list_quantity:
            if item[1] not in quantity_dict.keys():
                quantity_dict[item[1]] = item[0]
            else:
                quantity_dict[item[1]] += item[0]
        colors_dict = Counter(flat_list_colors)

        s = sum(cities_sell_dict.values())
        cities_percentage = {}
        for k, v in cities_sell_dict.items():
            try:
                pct = v * 100.0 / s
                cities_percentage[k] = round(pct, 2)
            except ZeroDivisionError:
                continue
        s = sum(users_dict.values())
        users_percentage = {}
        for k, v in users_dict.items():
            pct = v * 100.0 / s
            users_percentage[k] = round(pct, 2)
        cities_chart_color2 = {}

        for city, percentage in cities_percentage.items():
            cities_chart_color2[city] = '#' + ''.join(random.sample(chars, 6))
        for key in products_price_dict:
            products_price_dict[key] = f'{products_price_dict[key]:,}'
        context['users_dict_price'] = dict(sorted(users_dict_price.items(), key=lambda item: item[1]))
        context['cities_chart_color'] = cities_chart_color2
        context['cities_sell_dict'] = dict(sorted(cities_percentage.items(), key=lambda item: item[1]))
        context['payment_type'] = dict(sorted(payment_type2.items(), key=lambda item: item[1]))
        context['users_percentage'] = dict(sorted(users_percentage.items(), key=lambda item: item[1]))
        context['products_price'] = products_price_dict
        context['quantity_products'] = quantity_dict
        context['popular_colors'] = dict(colors_dict)
        context['months_volume'] = sorted_month_dict
        context['total_price'] = f'{total_price:,}'
        return context
