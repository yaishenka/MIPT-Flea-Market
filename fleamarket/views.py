from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AbstractAd
from .forms import AbstractAdForm


def ads_list(request):
    ads = AbstractAd.objects.all()
    return render(request, 'fleamarket/ads_list.html', {'ads': ads})


@login_required
def create_ad(request):
    if request.method == 'POST':
        create_form = AbstractAdForm(request.POST, request.FILES)
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
    if ad.seller != request.user:
        return redirect('ads_list')
    if request.method == "POST":
        form = AbstractAdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            print(form.cleaned_data['image'])
            form.save()
            return redirect('view_ad', pk=ad.pk)
    else:
        form = AbstractAdForm(instance=ad)
    return render(request, 'fleamarket/ad_edit.html', {'form': form})

@login_required
def delete_ad(request, pk):
    ad = get_object_or_404(AbstractAd, pk=pk)
    if ad.seller != request.user:
        return redirect('view_ad', pk=pk)

    ad = get_object_or_404(AbstractAd, pk=pk)
    ad.delete()
    return redirect('ads_list')


def view_ad(request, pk):
    ad = get_object_or_404(AbstractAd, pk=pk)
    return render(request, 'fleamarket/ad.html', {'ad': ad})
