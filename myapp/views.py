from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.http import JsonResponse
from .models import (
    Farmer, Admin, Customer, Worker, Delivery, DeliveryOrder,
    MarketSettings, Product, BargainingBid, FarmerWallet, AdminWallet, Sale
)
from .forms import (
    FarmerRegistrationForm, FarmerLoginForm, FarmerProfileForm, AdminLoginForm,
    CustomerRegistrationForm, CustomerLoginForm, CustomerProfileForm,
    WorkerRegistrationForm, WorkerLoginForm, WorkerProfileForm,
    DeliveryRegistrationForm, DeliveryLoginForm, DeliveryProfileForm, AdminDeliveryForm,
    MarketSettingsForm, ProductForm, BidForm
)


# ====================================================
# SESSION HELPERS & SECURITY ROUTING
# ====================================================

def get_current_farmer(request):
    farmer_id = request.session.get('farmer_id')
    if not farmer_id:
        return None
    try:
        return Farmer.objects.get(farmer_id=farmer_id)
    except Farmer.DoesNotExist:
        return None

def get_current_admin(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return None
    try:
        return Admin.objects.get(id=admin_id)
    except Admin.DoesNotExist:
        return None

def get_current_customer(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return None
    try:
        return Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return None

def get_current_worker(request):
    worker_id = request.session.get('worker_id')
    if not worker_id:
        return None
    try:
        return Worker.objects.get(worker_id=worker_id)
    except Worker.DoesNotExist:
        return None

def get_current_delivery(request):
    delivery_id = request.session.get('delivery_id')
    if not delivery_id:
        return None
    try:
        return Delivery.objects.get(delivery_id=delivery_id)
    except Delivery.DoesNotExist:
        return None

def get_active_session_redirect(request):
    """Returns redirect response if any active user session exists, else None."""
    if request.session.get('farmer_id'):
        return redirect('dashboard')
    if request.session.get('customer_id'):
        return redirect('customer_dashboard')
    if request.session.get('worker_id'):
        return redirect('worker_dashboard')
    if request.session.get('delivery_id'):
        return redirect('delivery_dashboard')
    if request.session.get('admin_id'):
        return redirect('admin_dashboard')
    return None

def clear_all_sessions(request):
    """Utility to pop all role session keys before logging in a specific role."""
    for key in ['farmer_id', 'farmer_email', 'farmer_name',
                'customer_id', 'customer_email', 'customer_name',
                'worker_id', 'worker_email', 'worker_name',
                'delivery_id', 'delivery_email', 'delivery_name',
                'admin_id', 'admin_email', 'admin_name']:
        request.session.pop(key, None)


# ====================================================
# PUBLIC VIEWS
# ====================================================

def home_view(request):
    current_farmer = get_current_farmer(request)
    current_admin = get_current_admin(request)
    current_customer = get_current_customer(request)
    current_worker = get_current_worker(request)
    current_delivery = get_current_delivery(request)

    return render(request, 'myapp/home.html', {
        'current_farmer': current_farmer,
        'current_admin': current_admin,
        'current_customer': current_customer,
        'current_worker': current_worker,
        'current_delivery': current_delivery,
    })

def choose_login_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect:
        return active_redirect
    return render(request, 'myapp/choose_login.html')


# ====================================================
# FARMER MODULE VIEWS
# ====================================================

def register_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('farmer_id'):
        messages.warning(request, "Please logout of your current session before registering a new account.")
        return active_redirect
    if request.session.get('farmer_id'):
        return redirect('dashboard')

    if request.method == 'POST':
        form = FarmerRegistrationForm(request.POST)
        if form.is_valid():
            farmer = form.save(commit=False)
            raw_password = form.cleaned_data.get('password')
            farmer.password = make_password(raw_password)
            farmer.save()
            messages.success(request, f"Registration successful! Your Farmer ID is {farmer.farmer_id}. Please log in.")
            return redirect('farmer_login')
    else:
        form = FarmerRegistrationForm()
    
    return render(request, 'myapp/register.html', {'form': form})

def login_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('farmer_id'):
        messages.warning(request, "You are already logged in with another user session.")
        return active_redirect
    if request.session.get('farmer_id'):
        return redirect('dashboard')

    error_message = None
    if request.method == 'POST':
        form = FarmerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                farmer = Farmer.objects.get(email=email)
                if check_password(password, farmer.password):
                    clear_all_sessions(request)
                    request.session['farmer_id'] = farmer.farmer_id
                    request.session['farmer_email'] = farmer.email
                    request.session['farmer_name'] = farmer.full_name
                    messages.success(request, f"Welcome back, {farmer.full_name}!")
                    return redirect('dashboard')
                else:
                    error_message = "Invalid Email or Password"
            except Farmer.DoesNotExist:
                error_message = "Invalid Email or Password"
    else:
        form = FarmerLoginForm()

    return render(request, 'myapp/login.html', {'form': form, 'error_message': error_message})

def dashboard_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('farmer_id'):
        messages.error(request, "Access denied to Farmer Dashboard.")
        return active_redirect

    farmer = get_current_farmer(request)
    if not farmer:
        messages.error(request, "Please log in to access the dashboard.")
        return redirect('farmer_login')

    context = {
        'farmer': farmer,
        'profile_status': 'Active',
    }
    return render(request, 'myapp/dashboard.html', context)

def profile_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('farmer_id'):
        messages.error(request, "Access denied to Farmer Profile.")
        return active_redirect

    farmer = get_current_farmer(request)
    if not farmer:
        messages.error(request, "Please log in to access your profile.")
        return redirect('farmer_login')

    if request.method == 'POST':
        form = FarmerProfileForm(request.POST, instance=farmer)
        if form.is_valid():
            form.save()
            request.session['farmer_name'] = farmer.full_name
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = FarmerProfileForm(instance=farmer)

    context = {
        'farmer': farmer,
        'form': form
    }
    return render(request, 'myapp/profile.html', context)

def logout_view(request):
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect('farmer_login')


# ====================================================
# CUSTOMER MODULE VIEWS
# ====================================================

def customer_register_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('customer_id'):
        messages.warning(request, "Please logout of your current session before registering a new account.")
        return active_redirect
    if request.session.get('customer_id'):
        return redirect('customer_dashboard')

    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            raw_password = form.cleaned_data.get('password')
            customer.password = make_password(raw_password)
            customer.save()
            messages.success(request, f"Registration successful! Your Customer ID is {customer.customer_id}. Please log in.")
            return redirect('customer_login')
    else:
        form = CustomerRegistrationForm()

    return render(request, 'myapp/customer_register.html', {'form': form})

def customer_login_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('customer_id'):
        messages.warning(request, "You are already logged in with another user session.")
        return active_redirect
    if request.session.get('customer_id'):
        return redirect('customer_dashboard')

    error_message = None
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                customer = Customer.objects.get(email=email)
                if check_password(password, customer.password):
                    clear_all_sessions(request)
                    request.session['customer_id'] = customer.customer_id
                    request.session['customer_email'] = customer.email
                    request.session['customer_name'] = customer.full_name
                    messages.success(request, f"Welcome back, {customer.full_name}!")
                    return redirect('customer_dashboard')
                else:
                    error_message = "Invalid Email or Password"
            except Customer.DoesNotExist:
                error_message = "Invalid Email or Password"
    else:
        form = CustomerLoginForm()

    return render(request, 'myapp/customer_login.html', {'form': form, 'error_message': error_message})

def customer_dashboard_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('customer_id'):
        messages.error(request, "Access denied to Customer Dashboard.")
        return active_redirect

    customer = get_current_customer(request)
    if not customer:
        messages.error(request, "Please log in to access the dashboard.")
        return redirect('customer_login')

    purchases = Sale.objects.filter(customer=customer).order_by('-sale_date')
    total_spent = sum([s.total_amount for s in purchases]) if purchases else Decimal('0.00')

    context = {
        'customer': customer,
        'profile_status': 'Active',
        'purchases': purchases,
        'total_spent': total_spent,
    }
    return render(request, 'myapp/customer_dashboard.html', context)


def customer_profile_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('customer_id'):
        messages.error(request, "Access denied to Customer Profile.")
        return active_redirect

    customer = get_current_customer(request)
    if not customer:
        messages.error(request, "Please log in to access your profile.")
        return redirect('customer_login')

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            request.session['customer_name'] = customer.full_name
            messages.success(request, "Profile updated successfully!")
            return redirect('customer_profile')
    else:
        form = CustomerProfileForm(instance=customer)

    context = {
        'customer': customer,
        'form': form
    }
    return render(request, 'myapp/customer_profile.html', context)

def customer_logout_view(request):
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect('customer_login')


def customer_live_rooms_view(request):
    customer = get_current_customer(request)
    if not customer:
        messages.error(request, "Please log in to access live rooms.")
        return redirect('customer_login')

    live_products = Product.objects.filter(status='AVAILABLE').order_by('-created_at')
    
    context = {
        'customer': customer,
        'live_products': live_products,
    }
    return render(request, 'myapp/customer_live_rooms.html', context)


def customer_bids_view(request):
    customer = get_current_customer(request)
    if not customer:
        messages.error(request, "Please log in to access your bids.")
        return redirect('customer_login')

    # Get unique products the customer bid on
    bid_products = Product.objects.filter(bids__customer=customer).distinct().order_by('-created_at')

    context = {
        'customer': customer,
        'bid_products': bid_products,
    }
    return render(request, 'myapp/customer_bids.html', context)


# ====================================================
# WORKER MODULE VIEWS
# ====================================================

def worker_register_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('worker_id'):
        messages.warning(request, "Please logout of your current session before registering a new account.")
        return active_redirect
    if request.session.get('worker_id'):
        return redirect('worker_dashboard')

    if request.method == 'POST':
        form = WorkerRegistrationForm(request.POST)
        if form.is_valid():
            worker = form.save(commit=False)
            raw_password = form.cleaned_data.get('password')
            worker.password = make_password(raw_password)
            worker.save()
            messages.success(request, f"Registration successful! Your Worker ID is {worker.worker_id}. Please log in.")
            return redirect('worker_login')
    else:
        form = WorkerRegistrationForm()

    return render(request, 'myapp/worker_register.html', {'form': form})

def worker_login_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('worker_id'):
        messages.warning(request, "You are already logged in with another user session.")
        return active_redirect
    if request.session.get('worker_id'):
        return redirect('worker_dashboard')

    error_message = None
    if request.method == 'POST':
        form = WorkerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                worker = Worker.objects.get(email=email)
                if check_password(password, worker.password):
                    clear_all_sessions(request)
                    request.session['worker_id'] = worker.worker_id
                    request.session['worker_email'] = worker.email
                    request.session['worker_name'] = worker.full_name
                    messages.success(request, f"Welcome back, {worker.full_name}!")
                    return redirect('worker_dashboard')
                else:
                    error_message = "Invalid Email or Password"
            except Worker.DoesNotExist:
                error_message = "Invalid Email or Password"
    else:
        form = WorkerLoginForm()

    return render(request, 'myapp/worker_login.html', {'form': form, 'error_message': error_message})

def worker_dashboard_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('worker_id'):
        messages.error(request, "Access denied to Worker Dashboard.")
        return active_redirect

    worker = get_current_worker(request)
    if not worker:
        messages.error(request, "Please log in to access the dashboard.")
        return redirect('worker_login')

    context = {
        'worker': worker,
        'profile_status': 'Active',
    }
    return render(request, 'myapp/worker_dashboard.html', context)

def worker_profile_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('worker_id'):
        messages.error(request, "Access denied to Worker Profile.")
        return active_redirect

    worker = get_current_worker(request)
    if not worker:
        messages.error(request, "Please log in to access your profile.")
        return redirect('worker_login')

    if request.method == 'POST':
        form = WorkerProfileForm(request.POST, instance=worker)
        if form.is_valid():
            form.save()
            request.session['worker_name'] = worker.full_name
            messages.success(request, "Profile updated successfully!")
            return redirect('worker_profile')
    else:
        form = WorkerProfileForm(instance=worker)

    context = {
        'worker': worker,
        'form': form
    }
    return render(request, 'myapp/worker_profile.html', context)

def worker_logout_view(request):
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect('worker_login')


# ====================================================
# DELIVERY PERSON MODULE VIEWS
# ====================================================


def delivery_login_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('delivery_id'):
        messages.warning(request, "You are already logged in with another user session.")
        return active_redirect
    if request.session.get('delivery_id'):
        return redirect('delivery_dashboard')

    error_message = None
    if request.method == 'POST':
        form = DeliveryLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                delivery = Delivery.objects.get(email=email)
                if check_password(password, delivery.password):
                    clear_all_sessions(request)
                    request.session['delivery_id'] = delivery.delivery_id
                    request.session['delivery_email'] = delivery.email
                    request.session['delivery_name'] = delivery.full_name
                    messages.success(request, f"Welcome back, {delivery.full_name}!")
                    return redirect('delivery_dashboard')
                else:
                    error_message = "Invalid Email or Password"
            except Delivery.DoesNotExist:
                error_message = "Invalid Email or Password"
    else:
        form = DeliveryLoginForm()

    return render(request, 'myapp/delivery_login.html', {'form': form, 'error_message': error_message})

def delivery_dashboard_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('delivery_id'):
        messages.error(request, "Access denied to Delivery Dashboard.")
        return active_redirect

    delivery = get_current_delivery(request)
    if not delivery:
        messages.error(request, "Please log in to access the dashboard.")
        return redirect('delivery_login')

    assigned_orders = delivery.assigned_deliveries.exclude(status='DELIVERED').order_by('-created_at')
    completed_orders = delivery.assigned_deliveries.filter(status='DELIVERED').order_by('-updated_at')

    context = {
        'delivery': delivery,
        'profile_status': 'Active',
        'assigned_orders': assigned_orders,
        'completed_orders': completed_orders,
    }
    return render(request, 'myapp/delivery_dashboard.html', context)

def delivery_update_status_view(request, order_id):
    delivery = get_current_delivery(request)
    if not delivery:
        return redirect('delivery_login')

    if request.method == 'POST':
        new_status = request.POST.get('status')
        order = get_object_or_404(DeliveryOrder, order_id=order_id, delivery_person=delivery)
        
        if new_status in [s[0] for s in DeliveryOrder.STATUS_CHOICES]:
            order.status = new_status
            order.save()
            if new_status == 'DELIVERED':
                delivery.status = 'AVAILABLE'
                delivery.save()
            messages.success(request, f"Delivery status updated to {new_status}")
    
    return redirect('delivery_dashboard')

def delivery_profile_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('delivery_id'):
        messages.error(request, "Access denied to Delivery Profile.")
        return active_redirect

    delivery = get_current_delivery(request)
    if not delivery:
        messages.error(request, "Please log in to access your profile.")
        return redirect('delivery_login')

    if request.method == 'POST':
        form = DeliveryProfileForm(request.POST, instance=delivery)
        if form.is_valid():
            form.save()
            request.session['delivery_name'] = delivery.full_name
            messages.success(request, "Profile updated successfully!")
            return redirect('delivery_profile')
    else:
        form = DeliveryProfileForm(instance=delivery)

    context = {
        'delivery': delivery,
        'form': form
    }
    return render(request, 'myapp/delivery_profile.html', context)

def delivery_logout_view(request):
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect('delivery_login')


# ====================================================
# ADMIN MODULE VIEWS
# ====================================================

def admin_login_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('admin_id'):
        messages.error(request, "Regular users cannot access Admin Dashboard.")
        return active_redirect
    if request.session.get('admin_id'):
        return redirect('admin_dashboard')

    error_message = None
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                admin = Admin.objects.get(email=email)
                if check_password(password, admin.password) or admin.password == password:
                    clear_all_sessions(request)
                    request.session['admin_id'] = admin.id
                    request.session['admin_email'] = admin.email
                    request.session['admin_name'] = admin.name
                    messages.success(request, f"Welcome back, {admin.name}!")
                    return redirect('admin_dashboard')
                else:
                    error_message = "Invalid Email or Password"
            except Admin.DoesNotExist:
                error_message = "Invalid Email or Password"
    else:
        form = AdminLoginForm()

    return render(request, 'myapp/admin_login.html', {'form': form, 'error_message': error_message})

def admin_dashboard_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('admin_id'):
        messages.error(request, "Regular users cannot access Admin Dashboard.")
        return active_redirect

    admin = get_current_admin(request)
    if not admin:
        messages.error(request, "Please log in as Admin to access the Admin Dashboard.")
        return redirect('admin_login')

    total_farmers = Farmer.objects.count()
    active_farmers = total_farmers
    
    today = timezone.now().date()
    new_registrations = Farmer.objects.filter(
        joining_date__year=today.year,
        joining_date__month=today.month
    ).count()

    products = Product.objects.all().order_by('-created_at')
    sales = Sale.objects.all().order_by('-sale_date')

    context = {
        'admin': admin,
        'total_farmers': total_farmers,
        'active_farmers': active_farmers,
        'new_registrations': new_registrations,
        'products': products,
        'sales': sales,
    }
    return render(request, 'myapp/admin_dashboard.html', context)


def admin_farmers_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('admin_id'):
        messages.error(request, "Regular users cannot access Admin Dashboard.")
        return active_redirect

    admin = get_current_admin(request)
    if not admin:
        messages.error(request, "Please log in as Admin to access the Farmers list.")
        return redirect('admin_login')

    farmers = Farmer.objects.all().order_by('-id')
    context = {
        'admin': admin,
        'farmers': farmers,
    }
    return render(request, 'myapp/admin_farmer_list.html', context)

def admin_farmer_detail_view(request, pk):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('admin_id'):
        messages.error(request, "Regular users cannot access Admin Dashboard.")
        return active_redirect

    admin = get_current_admin(request)
    if not admin:
        messages.error(request, "Please log in as Admin to view farmer details.")
        return redirect('admin_login')

    farmer = get_object_or_404(Farmer, pk=pk)
    context = {
        'admin': admin,
        'farmer': farmer,
    }
    return render(request, 'myapp/admin_farmer_detail.html', context)

def admin_logout_view(request):
    request.session.flush()
    messages.info(request, "Admin logged out successfully.")
    return redirect('admin_login')


def admin_customers_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('admin_id'):
        messages.error(request, "Only Administrator can view customers.")
        return active_redirect
    
    customers = Customer.objects.all().order_by('-joining_date')
    return render(request, 'myapp/admin_customers.html', {'customers': customers})

def admin_customer_detail_view(request, customer_id):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('admin_id'):
        return active_redirect
    
    customer = get_object_or_404(Customer, customer_id=customer_id)
    return render(request, 'myapp/admin_customer_detail.html', {'customer': customer})

def admin_deliveries_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('admin_id'):
        messages.error(request, "Only Administrator can view delivery personnel.")
        return active_redirect
    
    deliveries = Delivery.objects.all().order_by('-joining_date')
    orders = DeliveryOrder.objects.all().order_by('-created_at')
    return render(request, 'myapp/admin_deliveries.html', {'deliveries': deliveries, 'orders': orders})

def admin_delivery_detail_view(request, delivery_id):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('admin_id'):
        return active_redirect
    
    delivery = get_object_or_404(Delivery, delivery_id=delivery_id)
    return render(request, 'myapp/admin_delivery_detail.html', {'delivery': delivery})

def admin_add_delivery_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('admin_id'):
        messages.error(request, "Only Administrator can add delivery personnel.")
        return active_redirect
    
    if request.method == 'POST':
        form = AdminDeliveryForm(request.POST)
        if form.is_valid():
            delivery = form.save(commit=False)
            pwd = form.cleaned_data.get('password')
            if pwd:
                delivery.password = make_password(pwd)
            delivery.save()
            messages.success(request, f"Delivery Person {delivery.full_name} added successfully.")
            return redirect('admin_deliveries')
    else:
        form = AdminDeliveryForm()
        
    return render(request, 'myapp/admin_delivery_form.html', {'form': form, 'title': 'Add Delivery Person'})

def admin_edit_delivery_view(request, delivery_id):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('admin_id'):
        return active_redirect
    
    delivery = get_object_or_404(Delivery, delivery_id=delivery_id)
    if request.method == 'POST':
        form = AdminDeliveryForm(request.POST, instance=delivery)
        if form.is_valid():
            del_obj = form.save(commit=False)
            pwd = form.cleaned_data.get('password')
            if pwd and not pwd.startswith('pbkdf2_'):
                del_obj.password = make_password(pwd)
            del_obj.save()
            messages.success(request, f"Delivery Person {delivery.full_name} updated successfully.")
            return redirect('admin_deliveries')
    else:
        form = AdminDeliveryForm(instance=delivery)
        
    return render(request, 'myapp/admin_delivery_form.html', {'form': form, 'title': 'Edit Delivery Person'})

def admin_toggle_delivery_view(request, delivery_id):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('admin_id'):
        return active_redirect
    
    delivery = get_object_or_404(Delivery, delivery_id=delivery_id)
    if delivery.status == 'INACTIVE':
        delivery.status = 'AVAILABLE'
        msg = "activated"
    else:
        delivery.status = 'INACTIVE'
        msg = "deactivated"
    delivery.save()
    messages.success(request, f"Delivery Person {delivery.full_name} has been {msg}.")
    return redirect('admin_deliveries')

def admin_assign_delivery_view(request, order_id):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('admin_id'):
        return active_redirect
    
    order = get_object_or_404(DeliveryOrder, order_id=order_id, status='PENDING')
    available_deliveries = Delivery.objects.filter(status='AVAILABLE')
    
    return render(request, 'myapp/admin_assign_delivery.html', {
        'order': order,
        'available_deliveries': available_deliveries
    })

def admin_assign_delivery_action_view(request, order_id):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('admin_id'):
        return active_redirect
        
    if request.method == 'POST':
        delivery_id = request.POST.get('delivery_id')
        order = get_object_or_404(DeliveryOrder, order_id=order_id)
        
        if order.status != 'PENDING':
            messages.error(request, f"This delivery has already been assigned.")
            return redirect('admin_deliveries')
            
        delivery = get_object_or_404(Delivery, delivery_id=delivery_id)
        
        if delivery.status == 'AVAILABLE':
            order.delivery_person = delivery
            order.status = 'ASSIGNED'
            order.save()
            
            delivery.status = 'BUSY'
            delivery.save()
            messages.success(request, f"Order {order.order_id} assigned to {delivery.full_name}.")
        else:
            messages.error(request, f"Selected Delivery Person not found or is not available.")
            
    return redirect('admin_deliveries')


# ====================================================
# MARKETPLACE MODULE VIEWS
# ====================================================

def admin_marketplace_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('admin_id'):
        messages.error(request, "Regular users cannot manage the Marketplace.")
        return active_redirect

    admin = get_current_admin(request)
    if not admin:
        messages.error(request, "Please log in as Administrator to access Marketplace settings.")
        return redirect('admin_login')

    market_settings = MarketSettings.get_settings()

    if request.method == 'POST':
        form = MarketSettingsForm(request.POST, instance=market_settings)
        if form.is_valid():
            form.save()
            messages.success(request, f"Market settings updated successfully. Status is now {market_settings.status}.")
            return redirect('admin_marketplace')
    else:
        form = MarketSettingsForm(instance=market_settings)

    all_products = Product.objects.all().order_by('-created_at')
    total_sales = Sale.objects.all().order_by('-sale_date')

    context = {
        'admin': admin,
        'market_settings': market_settings,
        'form': form,
        'products': all_products,
        'sales': total_sales,
    }
    return render(request, 'myapp/admin_marketplace.html', context)


def _process_sale(product, highest_bid):
    winning_customer = highest_bid.customer
    winning_price = Decimal(str(highest_bid.bid_price_per_unit))
    quantity = Decimal(str(product.quantity))
    total_amount = quantity * winning_price

    farmer_share = (total_amount * Decimal('0.80')).quantize(Decimal('0.01'))
    admin_commission = (total_amount * Decimal('0.20')).quantize(Decimal('0.01'))

    # Update Product Status & Reserved Winning Customer
    product.status = 'SOLD'
    product.winning_customer = winning_customer
    product.save()

    # Update Bids Status
    highest_bid.status = 'ACCEPTED'
    highest_bid.save()
    BargainingBid.objects.filter(product=product).exclude(id=highest_bid.id).update(status='OUTBID')

    # Automatic Wallet Updates (80% Farmer / 20% Admin split)
    farmer_wallet, _ = FarmerWallet.objects.get_or_create(farmer=product.farmer)
    farmer_wallet.balance = Decimal(str(farmer_wallet.balance)) + farmer_share
    farmer_wallet.save()

    # Get or create admin for commission wallet
    admin_obj = Admin.objects.first()
    if not admin_obj:
        admin_obj, _ = Admin.objects.get_or_create(
            email='admin@farmlinkerp.com',
            defaults={'name': 'System Administrator', 'password': 'admin'}
        )

    admin_wallet, _ = AdminWallet.objects.get_or_create(admin=admin_obj)
    admin_wallet.balance = Decimal(str(admin_wallet.balance)) + admin_commission
    admin_wallet.save()

    # Record in Sales Table
    sale = Sale.objects.create(
        product=product,
        farmer=product.farmer,
        customer=winning_customer,
        quantity=product.quantity,
        winning_price=winning_price,
        total_amount=total_amount,
        farmer_share=farmer_share,
        admin_commission=admin_commission
    )
    
    # Create Delivery Order
    DeliveryOrder.objects.create(sale=sale, status='PENDING')


def admin_market_action_view(request, action):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('admin_id'):
        messages.error(request, "Only Administrator can manage the market.")
        return active_redirect

    admin = get_current_admin(request)
    if not admin:
        messages.error(request, "Please log in as Administrator.")
        return redirect('admin_login')

    market_settings = MarketSettings.get_settings()
    
    if action == 'open_market':
        market_settings.status = 'OPEN'
        market_settings.product_registration_status = 'OPEN'
        market_settings.bargaining_status = 'NOT_STARTED'
        messages.success(request, "Market opened successfully. Farmers can now add products.")
    elif action == 'close_registration':
        market_settings.product_registration_status = 'CLOSED'
        messages.success(request, "Product registration closed. Farmers can no longer add products.")
    elif action == 'open_bargaining':
        market_settings.bargaining_status = 'ACTIVE'
        market_settings.product_registration_status = 'CLOSED'
        messages.success(request, "Live bargaining has been opened. Product registration is now closed, and customers can now place bids.")
    elif action == 'stop_bargaining':
        market_settings.status = 'CLOSED'
        market_settings.product_registration_status = 'CLOSED'
        market_settings.bargaining_status = 'STOPPED'
        available_products = Product.objects.filter(status='AVAILABLE')
        for product in available_products:
            highest_bid = BargainingBid.objects.filter(product=product).order_by('-bid_price_per_unit', '-created_at').first()
            if highest_bid:
                _process_sale(product, highest_bid)
            else:
                product.status = 'UNSOLD'
                product.save()
        messages.success(request, "Live bargaining has been stopped. Products with bids were sold, and unsold products were removed.")
    elif action == 'close_market':
        market_settings.status = 'CLOSED'
        market_settings.product_registration_status = 'CLOSED'
        market_settings.bargaining_status = 'NOT_STARTED'
        available_products = Product.objects.filter(status='AVAILABLE')
        for product in available_products:
            highest_bid = BargainingBid.objects.filter(product=product).order_by('-bid_price_per_unit', '-created_at').first()
            if highest_bid:
                _process_sale(product, highest_bid)
            else:
                product.status = 'UNSOLD'
                product.save()
        messages.success(request, "Market is completely closed. Products with bids were sold, and unsold products were removed.")
    else:
        messages.error(request, "Invalid market action.")
        return redirect('admin_marketplace')

    market_settings.save()
    return redirect('admin_marketplace')


def admin_wallet_view(request):
    active_redirect = get_active_session_redirect(request)
    if active_redirect and not request.session.get('admin_id'):
        messages.error(request, "Only Administrator can access Admin Wallet.")
        return active_redirect

    admin = get_current_admin(request)
    if not admin:
        messages.error(request, "Please log in as Administrator.")
        return redirect('admin_login')

    wallet, _ = AdminWallet.objects.get_or_create(admin=admin)
    sales = Sale.objects.all().order_by('-sale_date')

    context = {
        'admin': admin,
        'wallet': wallet,
        'sales': sales,
    }
    return render(request, 'myapp/admin_wallet.html', context)


def farmer_products_view(request):
    farmer = get_current_farmer(request)
    if not farmer:
        messages.error(request, "Please log in as Farmer to view your products.")
        return redirect('login')

    market_settings = MarketSettings.get_settings()
    products = Product.objects.filter(farmer=farmer).order_by('-created_at')

    context = {
        'farmer': farmer,
        'products': products,
        'market_settings': market_settings,
    }
    return render(request, 'myapp/farmer_products.html', context)


def farmer_add_product_view(request):
    farmer = get_current_farmer(request)
    if not farmer:
        messages.error(request, "Please log in as Farmer to add products.")
        return redirect('login')

    market_settings = MarketSettings.get_settings()

    if request.method == 'POST':
        if market_settings.product_registration_status != 'OPEN':
            messages.error(request, "Product registration is currently closed.")
            return render(request, 'myapp/farmer_add_product.html', {
                'farmer': farmer,
                'form': ProductForm(request.POST, request.FILES),
                'market_settings': market_settings,
            })

        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = farmer
            product.status = 'AVAILABLE'
            product.save()
            messages.success(request, f"Product '{product.product_name}' created successfully!")
            return redirect('farmer_products')
    else:
        form = ProductForm()

    context = {
        'farmer': farmer,
        'form': form,
        'market_settings': market_settings,
    }
    return render(request, 'myapp/farmer_add_product.html', context)


def farmer_edit_product_view(request, product_id):
    farmer = get_current_farmer(request)
    if not farmer:
        messages.error(request, "Please log in as Farmer.")
        return redirect('login')

    product = get_object_or_404(Product, product_id=product_id, farmer=farmer)
    market_settings = MarketSettings.get_settings()

    if product.status == 'SOLD':
        messages.error(request, "Sold products cannot be edited.")
        return redirect('farmer_products')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.product_name}' updated successfully.")
            return redirect('farmer_products')
    else:
        form = ProductForm(instance=product)

    context = {
        'farmer': farmer,
        'form': form,
        'product': product,
        'is_edit': True,
        'market_settings': market_settings,
    }
    return render(request, 'myapp/farmer_add_product.html', context)


def farmer_delete_product_view(request, product_id):
    farmer = get_current_farmer(request)
    if not farmer:
        messages.error(request, "Please log in as Farmer.")
        return redirect('login')

    product = get_object_or_404(Product, product_id=product_id, farmer=farmer)
    if product.status == 'SOLD':
        messages.error(request, "Cannot delete a product that is already sold.")
    else:
        pname = product.product_name
        product.delete()
        messages.success(request, f"Product '{pname}' deleted successfully.")

    return redirect('farmer_products')


def farmer_wallet_view(request):
    farmer = get_current_farmer(request)
    if not farmer:
        messages.error(request, "Please log in as Farmer to view your wallet.")
        return redirect('login')

    wallet, _ = FarmerWallet.objects.get_or_create(farmer=farmer)
    sales = Sale.objects.filter(farmer=farmer).order_by('-sale_date')

    context = {
        'farmer': farmer,
        'wallet': wallet,
        'sales': sales,
    }
    return render(request, 'myapp/farmer_wallet.html', context)


def explore_products_view(request):
    market_settings = MarketSettings.get_settings()

    if market_settings.status != 'OPEN':
        products = []
    else:
        products = Product.objects.filter(status='AVAILABLE').order_by('-created_at')

    context = {
        'market_settings': market_settings,
        'products': products,
        'current_customer': get_current_customer(request),
        'current_farmer': get_current_farmer(request),
        'current_admin': get_current_admin(request),
    }
    return render(request, 'myapp/explore_products.html', context)


def join_bargaining_view(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    customer = get_current_customer(request)
    farmer = get_current_farmer(request)
    admin = get_current_admin(request)

    # Allow farmer owner or admin to view bargaining room directly
    if farmer and product.farmer == farmer:
        return redirect('live_bargaining', product_id=product.product_id)
    if admin:
        return redirect('live_bargaining', product_id=product.product_id)

    # Block worker and delivery person
    if request.session.get('worker_id') or request.session.get('delivery_id'):
        messages.error(request, "Workers and Delivery Persons cannot participate in live bargaining.")
        return redirect('home')

    # If NOT logged in as Customer
    if not customer:
        context = {
            'product': product,
        }
        return render(request, 'myapp/join_bargaining_auth.html', context)

    # Customer is logged in -> Open Live Bargaining Room
    return redirect('live_bargaining', product_id=product.product_id)


def live_bargaining_view(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    customer = get_current_customer(request)
    farmer = get_current_farmer(request)
    admin = get_current_admin(request)
    worker = get_current_worker(request)
    delivery = get_current_delivery(request)

    if worker or delivery:
        messages.error(request, "Worker and Delivery Person cannot participate in live bargaining.")
        return redirect('home')

    # Check role & permissions
    is_owner_farmer = (farmer and product.farmer == farmer)
    is_admin = bool(admin)
    is_customer = bool(customer)

    # Non-owner farmers cannot bid or watch other farmers' bargaining rooms
    if farmer and not is_owner_farmer and not is_customer and not is_admin:
        messages.error(request, "Farmers can only watch bargaining rooms for their own products.")
        return redirect('farmer_products')

    if not (is_customer or is_owner_farmer or is_admin):
        return redirect('join_bargaining', product_id=product.product_id)

    market_settings = MarketSettings.get_settings()
    bids = BargainingBid.objects.filter(product=product).order_by('-bid_price_per_unit', '-created_at')
    highest_bid = bids.first()

    bid_form = BidForm()

    context = {
        'product': product,
        'market_settings': market_settings,
        'bids': bids,
        'highest_bid': highest_bid,
        'bid_form': bid_form,
        'is_customer': is_customer,
        'is_owner_farmer': is_owner_farmer,
        'is_admin': is_admin,
        'current_customer': customer,
        'current_farmer': farmer,
        'current_admin': admin,
    }
    return render(request, 'myapp/live_bargaining.html', context)


def api_get_bids_view(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    bids = BargainingBid.objects.filter(product=product).order_by('-bid_price_per_unit', '-created_at')
    highest_bid = bids.first()

    bids_data = []
    for bid in bids:
        bids_data.append({
            'bid_id': bid.bid_id,
            'customer_name': bid.customer.full_name,
            'customer_id': bid.customer.customer_id,
            'bid_price_per_unit': float(bid.bid_price_per_unit),
            'total_bid_amount': float(bid.total_bid_amount),
            'status': bid.status,
            'created_at': bid.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        })

    highest_data = None
    if highest_bid:
        highest_data = {
            'bid_id': highest_bid.bid_id,
            'customer_name': highest_bid.customer.full_name,
            'bid_price_per_unit': float(highest_bid.bid_price_per_unit),
            'total_bid_amount': float(highest_bid.total_bid_amount),
        }

    market_settings = MarketSettings.get_settings()

    return JsonResponse({
        'product_id': product.product_id,
        'product_status': product.status,
        'bargaining_status': market_settings.bargaining_status,
        'winning_customer': product.winning_customer.full_name if product.winning_customer else None,
        'winning_customer_id': product.winning_customer.customer_id if product.winning_customer else None,
        'highest_bid': highest_data,
        'bids': bids_data,
    })


def api_place_bid_view(request, product_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    customer = get_current_customer(request)
    if not customer:
        return JsonResponse({'error': 'Only registered customers can place bids.'}, status=403)

    market_settings = MarketSettings.get_settings()
    if market_settings.status != 'OPEN':
        return JsonResponse({'error': 'Marketplace is currently closed.'}, status=400)
    
    if market_settings.bargaining_status != 'ACTIVE':
        return JsonResponse({'error': 'Bargaining is not currently active.'}, status=400)

    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    if product.status == 'SOLD':
        return JsonResponse({'error': 'This product has already been sold.'}, status=400)

    try:
        bid_price = Decimal(request.POST.get('bid_price_per_unit', '0'))
    except Exception:
        return JsonResponse({'error': 'Invalid bid price.'}, status=400)

    if bid_price <= 0:
        return JsonResponse({'error': 'Bid price must be greater than 0.'}, status=400)

    # Save new bid
    new_bid = BargainingBid.objects.create(
        product=product,
        customer=customer,
        bid_price_per_unit=bid_price,
        status='ACTIVE'
    )

    return JsonResponse({
        'success': True,
        'message': f'Bid placed successfully at ₹{new_bid.bid_price_per_unit}/unit!',
        'bid_id': new_bid.bid_id,
        'bid_price_per_unit': float(new_bid.bid_price_per_unit),
        'total_bid_amount': float(new_bid.total_bid_amount),
    })


# Removed accept_bid_view and reject_bid_view as they are no longer needed
# since the market handles selling automatically when closed.


# ====================================================
# ADMIN SALES HISTORY VIEWS
# ====================================================

def admin_sales_history_view(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        messages.error(request, "Please log in as Admin.")
        return redirect('admin_login')

    sales = Sale.objects.select_related('product', 'farmer', 'customer').order_by('-sale_date')

    # Filtering logic
    product_query = request.GET.get('product', '').strip()
    farmer_query = request.GET.get('farmer', '').strip()
    customer_query = request.GET.get('customer', '').strip()
    date_query = request.GET.get('date', '').strip()

    if product_query:
        sales = sales.filter(product__product_name__icontains=product_query)
    if farmer_query:
        sales = sales.filter(farmer__full_name__icontains=farmer_query)
    if customer_query:
        sales = sales.filter(customer__full_name__icontains=customer_query)
    if date_query:
        sales = sales.filter(sale_date__date=date_query)

    context = {
        'sales': sales,
        'product_query': product_query,
        'farmer_query': farmer_query,
        'customer_query': customer_query,
        'date_query': date_query,
    }
    return render(request, 'myapp/admin_sales_history.html', context)


def admin_sale_details_view(request, sale_id):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        messages.error(request, "Please log in as Admin.")
        return redirect('admin_login')

    sale = get_object_or_404(Sale.objects.select_related('product', 'farmer', 'customer'), sale_id=sale_id)

    context = {
        'sale': sale,
    }
    return render(request, 'myapp/admin_sale_details.html', context)


def admin_live_rooms_view(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        messages.error(request, "Please log in as Admin.")
        return redirect('admin_login')

    admin = get_current_admin(request)
    live_products = Product.objects.filter(status='AVAILABLE').order_by('-created_at')
    
    market_settings = MarketSettings.get_settings()
    
    products_data = []
    for product in live_products:
        bids = BargainingBid.objects.filter(product=product).order_by('-bid_price_per_unit', '-created_at')
        highest_bid = bids.first()
        products_data.append({
            'product': product,
            'bids_count': bids.count(),
            'highest_bid': highest_bid
        })

    context = {
        'admin': admin,
        'products_data': products_data,
        'market_settings': market_settings,
    }
    return render(request, 'myapp/admin_live_rooms.html', context)
