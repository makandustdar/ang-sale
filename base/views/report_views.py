from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.db.models import Count
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin

import random

from base.models import *
from product.models import *
from users.models import *


class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


class ReportList(ListView):
    model = Report
    template_name = "report/list.html"
    context_object_name = 'reports'
    paginate_by = 10
    ordering = '-create_date'


def report_add(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.method == 'POST':
        itemIds = request.POST.getlist('item')
        customer_request = request.POST.get('customerRequest')
        manager_decision = request.POST.get('managerDicision')
        final_decision = request.POST.get('finalDecision')

        if len(itemIds) > 0:
            report = Report.objects.create(order=order, customer_request=customer_request,
                                           manager_decision=manager_decision, final_decision=final_decision)

            for itemId in itemIds:
                productId = request.POST.get(f'product_{itemId}')
                product = Product.objects.get(id=productId)
                problem_count = request.POST.get(f'problemCount_{itemId}')
                quality_problem = request.POST.get(f'qualityProblem_{itemId}')

                DamagedProduct.objects.create(report=report, product=product, problem_count=problem_count,
                                              quality_problem=quality_problem)

            messages.success(request, 'شکایت ثبت شد')
            return redirect('admin_order_list')

    items = order.order_items.all()

    context = {'order': order, 'items': items}
    return render(request, 'report/add.html', context)


def report_detail(request, report_id):
    report = Report.objects.get(id=report_id)
    context = {'report': report}
    return render(request, 'report/detail.html', context)
