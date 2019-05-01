from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from fleamarket.models import AbstractAd
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def control_subscriptions(request):
    user = request.user
    ad_categories = [category[0] for category in AbstractAd.CATEGORIES]
    available_subscriptions = Group.objects.filter(name__in=ad_categories)
    user_subscriptions = user.groups.all()
    return render(request, 'subscriptions/control_subs.html',
                  {'available_subs': available_subscriptions,
                   'users_subs': user_subscriptions})

@login_required
def subscribe(request, subscription_id):
    user = request.user
    group = Group.objects.get(pk=subscription_id)
    user.groups.add(group)
    return redirect('control_subs')

@login_required
def unsubscribe(request, subscription_id):
    user = request.user
    group = Group.objects.get(pk=subscription_id)
    user.groups.remove(group)
    return redirect('control_subs')