from django.db import models
from django.contrib.auth.models import User
from django import forms
# Create your models here.

MEMBER_ROLE_CHOICES=(
    ('L1', u'Sales'),
    ('L2', u'Manager'),
    ('L3', u'Account'),
)

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u'名字')
    role = models.CharField(max_length=10, choices=MEMBER_ROLE_CHOICES,
                             default='Sales', verbose_name=u'Role')
    def __str__(self):
        return u'%s-%s'%(self.name, self.role)

    def isSales(self):
        if self.user.is_superuser:
            return True
        return self.role == 'L1' or self.role == 'L2'


    def isManager(self):
        if self.user.is_superuser:
            return True
        return self.role == 'L2'

    def isAccount(self):
        if self.user.is_superuser:
            return True
        return self.role == 'L3'

class MemberForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    password=forms.CharField(label='Password', widget=forms.PasswordInput())
    name=forms.CharField(label='Name', max_length=50)
    role=forms.ChoiceField(label='Role', choices=MEMBER_ROLE_CHOICES)

    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.filter(username=username).count() > 0 :
            raise forms.ValidationError("User Name exists!!")
        return username


