from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'core'

urlpatterns = [
    # Auth
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(next_page='core:login'), name='logout'),

    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),

    # Orders (slug-based)
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('orders/<slug:slug>/update/', views.OrderUpdateView.as_view(), name='order_update'),
    path('orders/<slug:slug>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),

    # Kitchen
    path('kitchen/', views.KitchenQueueView.as_view(), name='kitchen_queue'),
    path('api/kitchen/queue/', views.api_kitchen_queue, name='api_kitchen_queue'),
    path('api/order/<slug:slug>/status/', views.api_update_order_status, name='api_update_order_status'),

    # Inventory (slug-based)
    path('inventory/', views.InventoryListView.as_view(), name='inventory_list'),
    path('inventory/create/', views.InventoryCreateView.as_view(), name='inventory_create'),
    path('inventory/<slug:slug>/update/', views.InventoryUpdateView.as_view(), name='inventory_update'),
    path('inventory/<slug:slug>/delete/', views.InventoryDeleteView.as_view(), name='inventory_delete'),

    # Staff
    path('staff/', views.StaffListView.as_view(), name='staff_list'),
    path('staff/create/', views.StaffCreateView.as_view(), name='staff_create'),
    path('staff/<int:pk>/update/', views.StaffUpdateView.as_view(), name='staff_update'),
    path('staff/<int:pk>/delete/', views.StaffDeleteView.as_view(), name='staff_delete'),

    # Reports & Export
    path('reports/', views.ReportsView.as_view(), name='reports'),
    path('export/orders/', views.export_orders_excel, name='export_orders'),

    # API Notifications
    path('api/notifications/', views.api_notifications, name='api_notifications'),
    path('api/notifications/<int:pk>/read/', views.api_mark_notification_read, name='api_notification_read'),
]