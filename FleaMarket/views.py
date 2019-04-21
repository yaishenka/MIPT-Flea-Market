from django.shortcuts import render, redirect
from .models import AbstractAd
from .forms import AbstractAdForm
from django.contrib.auth.decorators import login_required

def ads_list(request, categories=None):
    ads = AbstractAd.objects.all()
    return render(request, 'fleamarket/ads_list.html', {'ads': ads})

@login_required
def create_ad(request):
    if request.method == 'POST':
        create_form = AbstractAdForm(request.POST)
        if create_form.is_valid():
            new_ad = create_form.save(commit=False)
            new_ad.seller = request.user
            new_ad.save()
            return redirect('ads_list')
    else:
        create_form = AbstractAdForm()
    return render(request, 'fleamarket/new_ad.html', {'form': create_form})