from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncDate
from .models import Product, Category, Employee, Order, OrderItem
from django.shortcuts import get_object_or_404
from django.db.models import Q

# ------------------------------
# Authentication Views
# ------------------------------

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# ------------------------------
# Dashboard
# ------------------------------

@login_required
def dashboard(request):
    return render(request, 'store/dashboard.html')

# ------------------------------
# Stock Management
# ------------------------------

@login_required
def stock_list(request):
    query = request.GET.get('q', '')
    order_by = request.GET.get('order_by', 'name')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    products = products.order_by(order_by)

    return render(request, 'store/stock_list.html', {
        'products': products,
        'query': query,
        'order_by': order_by
    })

@login_required
def add_product(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        category_id = request.POST['category']
        price = float(request.POST['price'])
        cost_price = float(request.POST['cost_price'])
        quantity = int(request.POST['quantity'])

        category = get_object_or_404(Category, id=category_id)
        Product.objects.create(
            name=name,
            category=category,
            price=price,
            cost_price=cost_price,
            quantity=quantity
        )
        return redirect('stock_list')

    return render(request, 'store/add_product.html', {'categories': categories})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('stock_list')

# ------------------------------
# Employee Management
# ------------------------------

@login_required
def employee_list(request):
    query = request.GET.get('q', '')
    order_by = request.GET.get('order_by', 'user__username')

    employees = Employee.objects.select_related('user').all()

    if query:
        employees = employees.filter(user__username__icontains=query)

    employees = employees.order_by(order_by)

    return render(request, 'store/employee_list.html', {
        'employees': employees,
        'query': query,
        'order_by': order_by
    })

@login_required
def add_employee(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = User.objects.create_user(username=username, password=password)
        Employee.objects.create(user=user, role=role)
        return redirect('employee_list')

    return render(request, 'store/add_employee.html')

@login_required
def delete_employee(request, emp_id):
    employee = get_object_or_404(Employee, id=emp_id)
    employee.user.delete()  # Deletes both Employee and linked User
    return redirect('employee_list')

# ------------------------------
# Sales Summary
# ------------------------------

@login_required
def sales_summary(request):
    query = request.GET.get('q', '')
    order_by = request.GET.get('order_by', '-date')

    orders = Order.objects.select_related('employee').prefetch_related('items__product').order_by(order_by)

    if query:
        orders = orders.filter(employee__user__username__icontains=query)

    total_sales = sum(order.total_amount for order in orders)
    total_profit = 0

    for order in orders:
        for item in order.items.all():
            if item.product and item.product.cost_price is not None:
                profit = (item.subtotal - (item.product.cost_price * item.quantity))
                total_profit += profit

    return render(request, 'store/sales_summary.html', {
        'orders': orders,
        'total_sales': total_sales,
        'total_profit': total_profit,
        'query': query,
        'order_by': order_by
    })

# ------------------------------
#  Dashboard Analytics
# ------------------------------

@login_required
def dashboard_analytics(request):
    total_products = Product.objects.count()
    total_sales = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0

    # More accurate profit calculation
    total_profit_data = OrderItem.objects.annotate(
        profit=ExpressionWrapper(
            F('subtotal') - (F('product__cost_price') * F('quantity')),
            output_field=DecimalField()
        )
    ).aggregate(total_profit=Sum('profit'))
    total_profit = total_profit_data['total_profit'] or 0

    low_stock_items = Product.objects.filter(quantity__lte=5)

    # Category distribution
    category_data = Product.objects.values('category__name').annotate(count=Sum('quantity'))
    category_data = [
        {"name": item['category__name'], "count": item['count']} for item in category_data
    ]

    #  Weekly Sales
    today = timezone.now()
    last_week = today - timedelta(days=7)
    recent_orders = Order.objects.filter(date__gte=last_week)

    weekly_sales = recent_orders.annotate(day=TruncDate('date')).values('day').annotate(
        total=Sum('total_amount')
    ).order_by('day')
    weekly_sales = [{"date": str(entry['day']), "total": entry['total']} for entry in weekly_sales]

    return render(request, 'store/dashboard_analytics.html', {
        'total_products': total_products,
        'total_sales': total_sales,
        'total_profit': total_profit,
        'low_stock_items': low_stock_items,
        'category_data': category_data,
        'weekly_sales': weekly_sales,
    })

@login_required
def order_list(request):
    query = request.GET.get('q', '')
    order_by = request.GET.get('order_by', '-date')

    orders = Order.objects.select_related('customer', 'employee').prefetch_related('items__product')

    if query:
        orders = orders.filter(
            Q(customer__name__icontains=query) |
            Q(employee__user__username__icontains=query)
        )

    orders = orders.order_by(order_by)

    return render(request, 'store/billing_orders.html', {
        'orders': orders,
        'query': query,
        'order_by': order_by
    })


@login_required
def print_order_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/invoice_print.html', {'order': order})
