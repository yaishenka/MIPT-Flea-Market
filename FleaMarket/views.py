from django.shortcuts import render, redirect, get_object_or_404
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
            return redirect('view_ad', pk=new_ad.pk)
    else:
        create_form = AbstractAdForm()
    return render(request, 'fleamarket/new_ad.html', {'form': create_form})

@login_required
def change_ad(request, pk):
    ad = get_object_or_404(AbstractAd, pk=pk)
    if (ad.seller != request.user):
        return redirect('ads_list')
    if request.method == "POST":
        form = AbstractAdForm(request.POST, instance=ad)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.save()
            return redirect('view_ad', pk=ad.pk)
    else:
        form = AbstractAdForm(instance=ad)
    return render(request, 'fleamarket/ad_edit.html', {'form': form})

def view_ad(request, pk):
    ad = get_object_or_404(AbstractAd, pk=pk)
    return render(request, 'fleamarket/ad.html', {'ad' : ad})