from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm

from .models import *


class PrivateForm(forms.ModelForm):
    class Meta:
        model = Private
        fields = ['fname', 'lname', 'id_code']
        labels = {'fname': 'نام', 'lname': 'نام خانوادگی', 'id_code': 'کد ملی'}

    def clean_id_code(self):
        id_code = self.cleaned_data['id_code']
        if id_code and (len(id_code) != 10 or not id_code.isnumeric()):
            raise forms.ValidationError('کد ملی معتبر نیست')
        if id_code and Private.objects.filter(id_code=id_code).exists():
            raise forms.ValidationError('کدملی ثبت شده است')
        return id_code


class PrivateEditForm(forms.ModelForm):
    class Meta:
        model = Private
        fields = ['fname', 'lname', 'id_code']
        labels = {'fname': 'نام', 'lname': 'نام خانوادگی', 'id_code': 'کد ملی'}

    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        super(PrivateEditForm, self).__init__(*args, **kwargs)

    def clean_id_code(self):
        id_code = self.cleaned_data['id_code']
        if id_code and (len(id_code) != 10 or not id_code.isnumeric()):
            raise forms.ValidationError('کد ملی معتبر نیست')
        if id_code and Private.objects.filter(id_code=id_code).exclude(
                profile=self.kwargs['instance'].profile).exists():
            raise forms.ValidationError('کدملی ثبت شده است')
        return id_code


class LegalForm(forms.ModelForm):
    class Meta:
        model = Legal
        fields = ['fname', 'lname', 'id_code',
                  'company_name', 'finance_code', 'phone']
        labels = {'fname': 'نام مدیرعامل', 'lname': 'نام خانوادگی مدیرعامل', 'id_code': 'شناسه ملی',
                  'company_name': 'نام شرکت / فروشگاه / سازمان', 'phone': 'شماره تماس', 'finance_code': 'کد اقتصادی'}

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) != 11 or not phone.isnumeric():
            raise forms.ValidationError('شماره تماس معتبر نیست')
        return phone

    def clean_id_code(self):
        id_code = self.cleaned_data['id_code']
        if id_code and not id_code.isnumeric():
            raise forms.ValidationError('شناسه ملی معتبر نیست')
        if Legal.objects.filter(id_code=id_code).exists():
            raise forms.ValidationError('شناسه ملی ثبت شده است')
        return id_code

    def clean_finance_code(self):
        finance_code = self.cleaned_data['finance_code']
        if not finance_code.isnumeric():
            raise forms.ValidationError('کد اقتصادی معتبر نیست')
        return finance_code


class LegalEditForm(forms.ModelForm):
    company_name = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    finance_code = forms.CharField(required=False)

    class Meta:
        model = Legal
        fields = ['fname', 'lname', 'id_code',
                  'company_name', 'finance_code', 'phone']
        labels = {'fname': 'نام مدیرعامل', 'lname': 'نام خانوادگی مدیرعامل', 'id_code': 'شناسه ملی',
                  'company_name': 'نام شرکت / فروشگاه / سازمان', 'phone': 'شماره تماس', 'finance_code': 'کد اقتصادی'}

    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        super(LegalEditForm, self).__init__(*args, **kwargs)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) != 11 or not phone.isnumeric():
            raise forms.ValidationError('شماره تماس معتبر نیست')
        return phone

    def clean_id_code(self):
        id_code = self.cleaned_data['id_code']
        if id_code and not id_code.isnumeric():
            raise forms.ValidationError('شناسه ملی معتبر نیست')
        if Legal.objects.filter(id_code=id_code).exclude(profile=self.kwargs['instance'].profile).exists():
            raise forms.ValidationError('شناسه ملی ثبت شده است')
        return id_code

    # def clean_finance_code(self):
    #     finance_code = self.cleaned_data['finance_code']
    #     if not finance_code.isnumeric():
    #         raise forms.ValidationError('کد اقتصادی معتبر نیست')
    #     return finance_code


class AdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {'username': 'نام کاربری',
                  'email': 'ایمیل'}

    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None


class ExpertForm(forms.ModelForm):
    class Meta:
        model = Expert
        fields = ['mobile', 'id_code']
        labels = {'mobile': 'شماره همراه', 'id_code': 'کدملی'}

    def clean_id_code(self):
        id_code = self.cleaned_data['id_code']
        if id_code and (len(id_code) != 10 or not id_code.isnumeric()):
            raise forms.ValidationError('کد ملی معتبر نیست')
        if id_code and Expert.objects.filter(id_code=id_code).exists():
            raise forms.ValidationError('کدملی ثبت شده است')
        return id_code

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if len(mobile) != 11 or not mobile.isnumeric():
            raise forms.ValidationError('شماره همراه معتبر نیست')
        if mobile and Expert.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError('شماره همراه ثبت شده است')
        return mobile


class ExpertEditForm(forms.ModelForm):
    class Meta:
        model = Expert
        fields = ['mobile', 'id_code']
        labels = {'mobile': 'شماره همراه', 'id_code': 'کدملی'}

    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        super(ExpertEditForm, self).__init__(*args, **kwargs)

    def clean_id_code(self):
        id_code = self.cleaned_data['id_code']
        if id_code and (len(id_code) != 10 or not id_code.isnumeric()):
            raise forms.ValidationError('کد ملی معتبر نیست')
        if id_code and Expert.objects.filter(id_code=id_code).exclude(user=self.kwargs['instance'].user).exists():
            raise forms.ValidationError('کدملی ثبت شده است')
        return id_code

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if len(mobile) != 11 or not mobile.isnumeric():
            raise forms.ValidationError('شماره همراه معتبر نیست')
        if mobile and Expert.objects.filter(mobile=mobile).exclude(user=self.kwargs['instance'].user).exists():
            raise forms.ValidationError('شماره همراه ثبت شده است')
        return mobile


class PasswordChangeForm(PasswordChangeForm):
    error_messages = {
        'password_incorrect': (
            "رمز عبور اشتباه است"
        ),
        'inactive': ("حساب کاربری غیرفعال است"),
        'password_mismatch': (
            'رمز عبور یکسان نیست'
        ),
        'password_too_similar': (
            'رمز عبور با نام کاربری مشابه است'
        ),
    }

    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = 'رمز عبور قبلی'
        self.fields['new_password1'].label = 'رمز عبور جدید'
        self.fields['new_password1'].help_text = None
        self.fields['new_password2'].label = 'تکرار رمز عبور جدید'


class ExhibitionForm(forms.ModelForm):
    class Meta:
        model = Exhibition
        fields = ['fname', 'lname', 'id_code', 'mobile', 'phone', 'address']
        labels = {'fname': 'نام', 'lname': 'نام خانوادگی', 'id_code': 'کد ملی',
                  'mobile': 'شماره همراه', 'phone': 'تلفن ثابت', 'address': ' آدرس'}

    def clean_id_code(self):
        id_code = self.cleaned_data['id_code']
        if id_code:
            if len(id_code) != 10 or not id_code.isnumeric():
                raise ValidationError('کد ملی نامعتبر است')
        return id_code

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if len(mobile) != 11 or not mobile.isnumeric():
            raise ValidationError('شماره همراه نامعتبر است')
        return mobile

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if len(phone) != 11 or not phone.isnumeric():
                raise ValidationError('تلفن ثابت نامعتبر است')
        return phone
