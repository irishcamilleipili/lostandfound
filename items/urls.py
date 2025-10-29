from django.urls import path
from . import views

urlpatterns = [
    # 🏠 Public pages
    path('', views.home_view, name='home'),
    path('items/', views.item_list, name='item_list'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),

    # 🛠️ CRUD operations
    path('create/', views.item_create, name='item_create'),
    path('item/<int:pk>/edit/', views.item_update, name='item_update'),
    path('item/<int:pk>/delete/', views.item_delete, name='item_delete'),

    # 🔐 Admin & Authentication
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-add-item/', views.admin_add_item, name='admin_add_item'),
    path('logout/', views.admin_logout, name='admin_logout'),

    # ⚡ AJAX or interactive endpoints
    path('item/<int:item_id>/toggle-status/', views.toggle_status, name='toggle_status'),
]
