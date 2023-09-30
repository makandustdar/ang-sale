from django.db import models
from django.contrib.auth.models import User


class State(models.Model):
    name = models.CharField(max_length=200)
    state_id = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=200)
    key = models.CharField(max_length=20)
    state = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    completed_percent = models.FloatField(default=0, blank=True, null=True)
    expert = models.ForeignKey('Expert', on_delete=models.SET_NULL, null=True, blank=True, related_name='customers')
    mobile = models.CharField(max_length=50)
    id_code = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.CharField(max_length=50, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    address = models.TextField()
    image = models.ImageField(upload_to="users/profile/images/", blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    login_code = models.CharField(max_length=10, blank=True, null=True)
    role = models.CharField(max_length=5, null=True)

    def __str__(self):
        return self.user.username

    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return None

    @property
    def get_user_role(self):
        if self.role == '1':
            return 'حقیقی'
        elif self.role == '2':
            return 'حقوقی'

    @property
    def get_full_name(self):
        if self.role == '1':
            return f'{self.private.fname} {self.private.lname}'
        elif self.role == '2':
            return f'{self.legal.fname} {self.legal.lname}'


class Private(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150)
    lname = models.CharField(max_length=150)
    id_code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f'{self.fname} {self.lname}'


class Legal(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150)
    lname = models.CharField(max_length=150)
    id_code = models.CharField(max_length=10, blank=True, null=True)
    company_name = models.CharField(max_length=150)
    finance_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.fname} {self.lname}'


class Expert(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=11)
    id_code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Exhibition(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=100)
    mobile = models.CharField(max_length=50)
    phone = models.CharField(max_length=50, blank=True, null=True)
    id_code = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.fname} {self.lname}'
