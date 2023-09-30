from django.shortcuts import render
from django.contrib import messages
from django.views.generic import ListView

from users.models import Exhibition
from users.forms import ExhibitionForm


class ExhibitionList(ListView):
    model = Exhibition
    template_name = "exhibition/list.html"
    context_object_name = 'users'
    ordering = '-create_date'
    paginate_by = 15


def add(request):
    if request.method == 'POST':
        form = ExhibitionForm(request.POST)
        if form.is_valid():
            id_code = form.cleaned_data['id_code']
            mobile = form.cleaned_data['mobile']

            if id_code and Exhibition.objects.filter(id_code=id_code).exists():
                messages.error(request, 'کاربر با این شماره ملی وجود دارد')
            elif Exhibition.objects.filter(mobile=mobile).exists():
                messages.error(request, 'کاربر با این شماره همراه وجود دارد')
            else:
                form.save()
                messages.success(request, 'کاربر افزوده شد')
    else:
        form = ExhibitionForm()

    users = Exhibition.objects.all().order_by('-create_date')[:5]
    context = {'form': form, 'users': users}
    return render(request, 'exhibition/add.html', context)


def edit(request, id):
    user = Exhibition.objects.get(id=id)
    if request.method == 'POST':
        form = ExhibitionForm(request.POST, instance=user)
        if form.is_valid():
            id_code = form.cleaned_data['id_code']
            mobile = form.cleaned_data['mobile']

            if id_code and Exhibition.objects.filter(id_code=id_code).exclude(id=id).exists():
                messages.error(request, 'کاربر با این شماره ملی وجود دارد')
            elif Exhibition.objects.filter(mobile=mobile).exclude(id=id).exists():
                messages.error(request, 'کاربر با این شماره همراه وجود دارد')
            else:
                form.save()
                messages.success(request, 'کاربر ویرایش شد')
    else:
        form = ExhibitionForm(request.POST or None, instance=user)

    context = {'form': form, 'user': user}
    return render(request, 'exhibition/edit.html', context)
