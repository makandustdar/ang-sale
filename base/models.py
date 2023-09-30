import time

from django.conf import settings
from django.urls import resolve, reverse
from django.utils import timezone

from product.models import *
from users.models import Expert


class Order(models.Model):
    PAYMENT_CHOICES = (
        ('CA', 'نقد'),
        ('CH1', 'چک یک ماهه'),
        ('CH2', 'چک دو ماهه'),
        ('CH3', 'چک سه ماهه'),
    )
    expert = models.ForeignKey(Expert, on_delete=models.SET_NULL, null=True, blank=True, related_name='expert_orders')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='user_orders')
    createdAt = models.DateTimeField(auto_now_add=True)
    order_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    track = models.CharField(max_length=10)
    transId = models.CharField(max_length=10)
    price = models.BigIntegerField(default=0)
    payment_type = models.CharField(max_length=3, choices=PAYMENT_CHOICES, default='CA')
    description = models.TextField(null=True, blank=True)
    confirmed = models.BooleanField(default=False)

    class META:
        ordering = ['createdAt']

    def __str__(self):
        return f"order {self.id}"

    @property
    def get_track(self):
        if self.track == 'REGISTER':
            return 'ثبت سفارش'
        elif self.track == 'HOLDING':
            return 'در انتظار تایید سفارش'
        elif self.track == 'PRODUCING':
            return 'در حال تولید'
        elif self.track == 'PAYING':
            return 'در انتظار تکمیل وجه'
        elif self.track == 'COMPLETE':
            return 'تکمیل سفارش'
        elif self.track == 'CANCEL':
            return 'لغو سفارش'
        else:
            return 'ثبت نشده'


class OrderConfirmationCode(models.Model):
    code = models.CharField(max_length=7)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f'confirmation code for order {self.order}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    productName = models.CharField(max_length=300)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    colorName = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    fee = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.productName}*{self.quantity}'


class OrderItemDetail(models.Model):
    orderitem = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.SET_NULL, null=True)
    featureName = models.CharField(max_length=300)
    featureValue = models.ForeignKey(FeatureValue, on_delete=models.SET_NULL, null=True)
    featureValueName = models.CharField(max_length=300)


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=300, null=True)
    text = models.CharField(max_length=500, null=True)
    userRead = models.BooleanField(default=False)
    adminRead = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Report(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    customer_request = models.CharField(max_length=500, blank=True, null=True)
    manager_decision = models.CharField(max_length=200, blank=True, null=True)
    final_decision = models.CharField(max_length=200, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)


class DamagedProduct(models.Model):
    report = models.ForeignKey(Report, on_delete=models.SET_NULL, null=True)
    orderitem = models.ForeignKey(
        OrderItem, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.CharField(max_length=10, blank=True, null=True)
    problem_count = models.CharField(max_length=5)
    quality_problem = models.CharField(max_length=100)


class Wallet(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.BigIntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return f'wallet number {self.id}|user {self.owner}'


class NameModel(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ActivityArea(NameModel):
    ...


class CustomerSource(NameModel):
    """
        for example sources are: from ads, from phone marketing, from email marketing ...
    """
    ...


class CustomerCurrentStatus(NameModel):
    ...


class SellOpportunityStatus(NameModel):
    ...


class Clue(models.Model):
    RATE_CHOICES = (
        ('C', 'سرد'),
        ('W', 'گرم'),
        ('H', 'داغ'),
    )
    title = models.CharField(max_length=200, blank=True, null=True)
    expert = models.OneToOneField(Expert, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    role = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    mobile = models.CharField(max_length=11, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    website = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    company_activity_area = models.OneToOneField(ActivityArea, on_delete=models.CASCADE, blank=True, null=True)
    staff_count = models.IntegerField(blank=True, null=True)
    source = models.OneToOneField(CustomerSource, on_delete=models.CASCADE, blank=True, null=True)
    rate = models.CharField(max_length=1, choices=RATE_CHOICES, blank=True, null=True)
    status = models.OneToOneField(CustomerCurrentStatus, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('clue_detail', kwargs={'clue_id': self.id})


class SellOpportunity(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    sell_date = models.DateField(blank=True, null=True)
    status = models.OneToOneField(SellOpportunityStatus, on_delete=models.CASCADE, blank=True, null=True)
    sell_probability = models.IntegerField(blank=True, null=True)
    expert = models.OneToOneField(Expert, on_delete=models.CASCADE, blank=True, null=True)
    total_price = models.CharField(max_length=200, blank=True, null=True)
    source = models.OneToOneField(CustomerSource, on_delete=models.CASCADE, blank=True, null=True)
    next_step = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('opportunity_detail', kwargs={'opportunity_id': self.id})
