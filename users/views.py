from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm
from django.contrib.auth import login, logout
from .backends import AuthBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from fleamarket.models import AbstractAd


def user_login(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        auth_backend = AuthBackend()
        try:
            user = auth_backend.authenticate(request=request,
                                             username=username,
                                             password=password)
            if user.is_active:
                login(request, user, backend='users.backends.AuthBackend')
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('ads_list')
        except get_user_model().DoesNotExist:
            error = 'Такой адрес или ник не существуют.'
            return render(request, 'cabinet/auth.html',
                          {'form': login_form, 'error': error})
        except ValidationError as e:
            error = 'Неверный пароль'
            return render(request, 'cabinet/auth.html',
                          {'form': login_form, 'error': error})

    else:
        if request.user.is_authenticated:
            return redirect('ads_list')
        login_form = AuthenticationForm()
    return render(request, 'users/login.html',
                  {'form': login_form, 'error': False})


def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return redirect('login')
        else:
            user_form = UserRegistrationForm()
            return render(request, 'users/register.html',
                          {'form': user_form,
                           'error': 'Данные введены с ошибкой'})
    else:
        if request.user.is_authenticated:
            return redirect('ads_list')
        user_form = UserRegistrationForm()
    return render(request, 'users/register.html',
                  {'form': user_form, 'error': False})


def user_logout(request):
    logout(request)
    return redirect('ads_list')


def user_view(request, user_id):
    user = get_object_or_404(get_user_model(), pk=user_id)
    users_ads = AbstractAd.objects.filter(seller=user)
    return render(request, 'users/user.html',
                  {'user_obj': user, 'users_ads': users_ads})


@login_required
def private_office(request):
    user = request.user
    users_subscriptions = user.groups.all()
    users_ads = AbstractAd.objects.filter(seller=user)
    return render(request, 'users/private_office.html',
                  {'user_obj': user, 'users_ads': users_ads,
                   'users_subscriptions': users_subscriptions})

