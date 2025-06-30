from django.urls import path
from . import views
from .views import dashboard_analytics

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Stock Management
    path('stock/', views.stock_list, name='stock_list'),
    path('stock/add/', views.add_product, name='add_product'),
    path('stock/delete/<int:product_id>/', views.delete_product, name='delete_product'),

    # Employee Management
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/delete/<int:emp_id>/', views.delete_employee, name='delete_employee'),

    path('sales/', views.sales_summary, name='sales_summary'),

    path('dashboard/analytics/', views.dashboard_analytics, name='dashboard_analytics'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/print/<int:order_id>/', views.print_order_invoice, name='print_order_invoice'),
]

