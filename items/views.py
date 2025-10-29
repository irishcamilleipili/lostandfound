from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Item
from .forms import ItemForm


# ----------------------------
# Public Views
# ----------------------------

def home_view(request):
    """
    Home page showing all reported items and the 'Report an Item' form toggle.
    """
    items = Item.objects.all().order_by('-date_reported')
    return render(request, 'invApp/home.html', {'items': items})


def item_list(request):
    """
    List of all reported items.
    """
    items = Item.objects.all().order_by('-date_reported')
    return render(request, 'invApp/item_list.html', {'items': items})


def item_detail(request, pk):
    """
    Detailed view for a single item.
    """
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'invApp/item_detail.html', {'item': item})


def item_create(request):
    """
    Handles creation of 'found' items directly from the public form.
    """
    items = Item.objects.filter(category='found').order_by('-date_reported')

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.category = 'found'
            item.save()
            return redirect('home')  # Redirect to home after submitting
    else:
        form = ItemForm()

    return render(request, 'invApp/home.html', {
        'form': form,
        'items': items
    })


def item_update(request, pk):
    """
    Edit existing item (used for admin panel).
    """
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'invApp/home.html', {'form': form})


@csrf_exempt
def item_delete(request, pk):
    """
    Deletes an item via normal POST or AJAX.
    """
    item = get_object_or_404(Item, pk=pk)

    if request.method == "POST":
        item.delete()

        # AJAX request → return JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})

        # Normal POST → redirect
        return redirect('admin_panel')

    return render(request, 'invApp/item_confirm_delete.html', {'item': item})


# ----------------------------
# Admin Login & Panel Views
# ----------------------------

def admin_login(request):
    """
    Custom admin login page using Django authentication.
    Redirects to admin_panel.html on success.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:  # Only staff can access admin panel
            login(request, user)
            return redirect("admin_panel")
        else:
            messages.error(request, "Invalid username or password")

    # ✅ Use the correct template path
    return render(request, "invApp/login.html")


@login_required(login_url="admin_login")
def admin_panel(request):
    """
    Custom admin dashboard for managing reported items.
    Only accessible to logged-in staff users.
    """
    if not request.user.is_staff:
        return redirect("admin_login")

    items = Item.objects.all().order_by('-date_reported')
    return render(request, "invApp/admin_panel.html", {'items': items})


@login_required(login_url="admin_login")
def admin_add_item(request):
    """
    Allows admin to add new found items directly from the admin panel.
    """
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.category = item.category or "found"
            item.save()
            messages.success(request, "New item added successfully!")
            return redirect("admin_panel")
    else:
        form = ItemForm()

    return render(request, "invApp/home.html", {"form": form})


def admin_logout(request):
    """
    Logs out the admin and redirects to login page.
    """
    logout(request)
    return redirect("admin_login")


# ----------------------------
# AJAX: Toggle Status (Pending ↔ Claimed)
# ----------------------------

@csrf_exempt
@require_POST
def toggle_status(request, item_id):
    """
    Toggle item status (Pending <-> Claimed) via AJAX.
    Returns JSON response for instant UI updates.
    """
    try:
        item = get_object_or_404(Item, id=item_id)
        item.status = "Claimed" if item.status == "Pending" else "Pending"
        item.save(update_fields=["status"])
        return JsonResponse({"status": item.status})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
