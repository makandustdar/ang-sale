from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import DetailView
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin

from users.forms import AdminForm, PasswordChangeForm
from users.models import Profile


# class ProfileDetailView(LoginRequiredMixin, DetailView):
#     model = Profile
#     context_object_name = 'profile'
#     template_name = 'base/profile.html'
#
#     def post(self, request, *args, **kwargs):
#         form = AdminForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(
#                 request, 'کاربر ادمین ویرایش شد')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data()
#         form = AdminForm(self.request.POST or None, instance=self.request.user)
#         context['form'] = form
#         return context


# @user_passes_test(lambda u: u.is_staff, login_url='/admin/login/')
# def profile(request):
#     if request.method == 'POST':
#         form = AdminForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(
#                 request, 'کاربر ادمین ویرایش شد')
#     else:
#         form = AdminForm(request.POST or None, instance=request.user)
#
#     context = {'form': form, 'profile': profile}
#     return render(request, 'profile/admin/profile.html', context)


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard_admin')
            else:
                messages.error(request, 'نام کاربری یا رمز عبور صحیح نمیباشد')
        else:
            messages.error(request, 'خطایی رخ داده است')
    return render(request, 'auth/admin/login.html')


@user_passes_test(lambda u: u.is_staff, login_url='/admin/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'رمز عبور باموفقیت ثبت شد')
            return redirect('change_password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'auth/admin/change_password.html', {
        'form': form
    })
