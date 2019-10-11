from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib.auth.models import User
from .models import Member, MemberForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages

def home(request):
    return render(request, 'statics/home_page.html')

def help_home(request):
    return render(request, 'statics/help_home.html')

def index(request):
    users = User.objects.filter(is_superuser=False).all()
    return render(request, 'members/index.html', {'users':users})

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

def member_login(request):
    if request.method == 'POST':
        try:
            loginForm = LoginForm(request.POST)
            if loginForm.is_valid():
                username = loginForm.cleaned_data['username']
                password = loginForm.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                login(request, user)
                messages.success(request, 'Member Login Successful !')
                return redirect(reverse('home'))
        except:
            messages.error(request, 'Member Login Failed ')

    else:
        loginForm = LoginForm()

    return render(request, 'members/members_login.html', {'form': loginForm})

def member_logout(request):
    logout(request)
    return redirect(reverse('home'))


def add(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password'],
                                            )
            member = Member.objects.create(user=user,
                                           name=form.cleaned_data['name'],
                                           role=form.cleaned_data['role']
                                           )
            return redirect(reverse('member_index'))
    else:
        form = MemberForm()

    return render(request, 'members/add.html',{'form': form})

from django import forms

def edit(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    form = MemberForm()
    form.fields['username'].widget=forms.HiddenInput()
    form.initial['username']='*&XSD'
    form.initial['name'] = member.name
    form.initial['role']=member.role

    if request.method=='POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member.name=form.cleaned_data['name']
            member.role = form.cleaned_data['role']
            member.save()
            return redirect(reverse('member_index'))

    return render(request, 'members/edit.html', {'member': member, 'form': form})
