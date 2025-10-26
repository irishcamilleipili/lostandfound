from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .forms import ItemForm


def home_view(request):
    items = Item.objects.all().order_by('-date_reported')
    return render(request, 'invApp/home.html', {'items': items})


def item_list(request):
    items = Item.objects.all().order_by('-date_reported')
    return render(request, 'invApp/item_list.html', {'items': items})


def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'invApp/item_detail.html', {'item': item})


def item_create(request):
    """
    Handles the Found Item creation and listing
    The category is automatically set to 'found'
    """
    # Show only found items on the right side
    items = Item.objects.filter(category='found').order_by('-date_reported')

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.category = 'found'  # 👈 Automatically tag it as found
            item.save()
            return redirect('item_create')  # Reload the page to show the new item
    else:
        form = ItemForm()

    return render(request, 'invApp/item_form.html', {
        'form': form,
        'items': items
    })


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
