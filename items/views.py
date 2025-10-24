from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .forms import ItemForm


def home_view(request):
    items = Item.objects.all()
    return render(request, 'invApp/home.html')

def item_list(request):
    items = Item.objects.all().order_by('-date_reported')
    return render(request, 'invApp/item_list.html', {'items': items})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'invApp/item_detail.html', {'item': item})

def item_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'invApp/item_form.html', {'form': form})

def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'invApp/item_form.html', {'form': form})

def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        item.delete()
        return redirect('item_list')
    return render(request, 'invApp/item_confirm_delete.html', {'item': item})