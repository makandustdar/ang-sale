from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Permission
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView

from users.forms import *
from base.utils import *


class ExpertList(PermissionRequiredMixin, ListView):
    model = Expert
    permission_required = 'admin.logentry'
    template_name = "expert/list.html"
    paginate_by = 10
    context_object_name = 'experts'
    ordering = '-user__date_joined'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ExpertList, self).get_context_data()
        experts = self.get_queryset()
        top_experts = experts.annotate(customers_count=Count('customers')).order_by('-customers_count')[:3]
        # print(top_experts.values('user__username', 'customers_count'))
        context['top_experts'] = top_experts
        return context


@permission_required('admin.logentry', login_url='/admin/login/')
def add(request):
    if request.method == 'POST':
        form = ExpertForm(request.POST)
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        permission_list = request.POST.getlist('permission')
        send_password = request.POST.get('send_password')

        if form.is_valid():
            if User.objects.filter(username=username).exists():
                messages.error(request, 'نام کاربری ثبت شده است')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if len(password) < 6:
                messages.error(request, 'رمز عبور کوتاه است')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user = User.objects.create(
                username=username, first_name=fname, last_name=lname, is_staff=True)
            user.set_password(password)
            user.save()
            cd = form.cleaned_data
            Profile.objects.create(user=user, mobile=cd['mobile'], id_code=cd['id_code'])
            instance = form.save(commit=False)
            instance.user = user
            instance.save()

            for permission in permission_list:
                user.user_permissions.add(Permission.objects.get(codename=permission))
            user.save()

            if send_password:
                send_password_to_expert(
                    instance.mobile, password, username)

            messages.success(request, 'کارشناس ایجاد شد')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = ExpertForm()

    context = {'form': form}
    return render(request, 'expert/add.html', context)


@permission_required('admin.logentry', login_url='/admin/login/')
def edit(request, expert_id):
    expert = Expert.objects.get(id=expert_id)
    if request.method == 'POST':
        form = ExpertEditForm(request.POST, instance=expert)
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        send_password = request.POST.get('send_password')
        permission_list = request.POST.getlist('permission')

        if form.is_valid():
            if User.objects.filter(username=username).exclude(expert__id=expert_id).exists():
                messages.error(request, 'نام کاربری ثبت شده است')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if password and len(password) < 6:
                messages.error(request, 'رمز عبور کوتاه است')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user = User.objects.get(expert__id=expert_id)
            user.username = username
            user.first_name = fname
            user.last_name = lname

            if password:
                user.set_password(password)
                if send_password:
                    send_password_to_expert(
                        expert.mobile, password, expert.username)
            if permission_list:
                user.user_permissions.clear()
                for permission in permission_list:
                    user.user_permissions.add(
                        Permission.objects.get(codename=permission))

            user.save()
            form.save()
            messages.success(request, 'کارشناس ویرایش شد')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = ExpertEditForm(request.POST or None, instance=expert)

    context = {'form': form, 'expert': expert}
    return render(request, 'expert/edit.html', context)


@login_required(login_url='/users/login/')
def transfer_customers(request, expert_id):
    to_expert = request.POST.get('to_expert')
    current_expert = Expert.objects.get(id=expert_id)
    target_expert = Expert.objects.get(id=to_expert)
    transfer_all = True if request.POST.get('transfer_all') == 'on' else False
    customers_list = request.POST.getlist('customers_list')

    if transfer_all:
        current_expert.customers.all().update(expert=target_expert)
        messages.success(request, f'کاربران {current_expert} با موفقیت به {target_expert} انتقال یافتند')
    elif customers_list:
        current_expert.customers.filter(id__in=customers_list).update(expert=target_expert)
        messages.success(request, f"{len(customers_list)} کاربر از {current_expert} به {target_expert} انتقال یافتند ")
    return redirect('expert_list')
