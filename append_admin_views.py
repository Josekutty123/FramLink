import os

# 1. Update URLs
urls_path = r"c:\Users\Asus\python-project\MCA_Project\myapp\urls.py"
with open(urls_path, 'r') as f:
    content = f.read()

admin_urls = """    path('admin/insurance/officers/', views.admin_officers_view, name='admin_officers'),
    path('admin/insurance/officers/add/', views.admin_add_officer_view, name='admin_add_officer'),
    path('admin/insurance/officers/toggle/<str:officer_id>/', views.admin_toggle_officer_view, name='admin_toggle_officer'),
    path('admin/insurance/dashboard/', views.admin_insurance_dashboard_view, name='admin_insurance_dashboard'),
    
    # Marketplace Module URLs"""

if 'admin_officers_view' not in content:
    content = content.replace("    # Marketplace Module URLs", admin_urls)
    with open(urls_path, 'w') as f:
        f.write(content)

# 2. Append Views
views_path = r"c:\Users\Asus\python-project\MCA_Project\myapp\views.py"
admin_views = """
# ====================================================
# AGRICULTURAL INSURANCE VIEWS - ADMIN
# ====================================================

def admin_officers_view(request):
    if not request.session.get('admin_id'):
        return redirect('admin_login')
        
    officers = InsuranceOfficer.objects.all().order_by('-created_at')
    return render(request, 'myapp/admin_officers.html', {'officers': officers})

def admin_add_officer_view(request):
    if not request.session.get('admin_id'):
        return redirect('admin_login')
        
    if request.method == 'POST':
        form = InsuranceOfficerForm(request.POST)
        if form.is_valid():
            officer = form.save(commit=False)
            officer.password = make_password(form.cleaned_data['password'])
            officer.save()
            messages.success(request, "Insurance Officer created successfully.")
            return redirect('admin_officers')
    else:
        form = InsuranceOfficerForm()
        
    return render(request, 'myapp/admin_add_officer.html', {'form': form})

def admin_toggle_officer_view(request, officer_id):
    if not request.session.get('admin_id'):
        return redirect('admin_login')
        
    officer = get_object_or_404(InsuranceOfficer, officer_id=officer_id)
    officer.is_active = not officer.is_active
    officer.save()
    messages.success(request, f"Officer {'activated' if officer.is_active else 'deactivated'} successfully.")
    return redirect('admin_officers')

def admin_insurance_dashboard_view(request):
    if not request.session.get('admin_id'):
        return redirect('admin_login')
        
    policies = InsurancePolicy.objects.all()
    enrollments = FarmerPolicyEnrollment.objects.all()
    payments = PremiumPayment.objects.all()
    claims = InsuranceClaim.objects.all()
    settlements = ClaimSettlement.objects.all()
    
    context = {
        'policies': policies,
        'enrollments': enrollments,
        'payments': payments,
        'claims': claims,
        'settlements': settlements
    }
    return render(request, 'myapp/admin_insurance_dashboard.html', context)
"""

with open(views_path, 'r') as f:
    if 'admin_officers_view' not in f.read():
        with open(views_path, 'a') as f_append:
            f_append.write(admin_views)

# 3. Create Templates
templates_dir = r"c:\Users\Asus\python-project\MCA_Project\myapp\templates\myapp"

admin_officers_html = """{% extends 'myapp/admin_base.html' %}
{% block title %}Manage Insurance Officers{% endblock %}
{% block admin_content %}
<div class="container-fluid p-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h3 class="fw-bold mb-0">Manage Insurance Officers</h3>
        <a href="{% url 'admin_add_officer' %}" class="btn btn-primary"><i class="bi bi-person-plus"></i> Add Officer</a>
    </div>
    
    <div class="card shadow-sm border-0">
        <div class="table-responsive">
            <table class="table table-hover mb-0">
                <thead class="table-light">
                    <tr>
                        <th>Officer ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for o in officers %}
                    <tr>
                        <td>{{ o.officer_id }}</td>
                        <td>{{ o.full_name }}</td>
                        <td>{{ o.email }}</td>
                        <td>{{ o.phone }}</td>
                        <td>
                            {% if o.is_active %}<span class="badge bg-success">Active</span>{% else %}<span class="badge bg-danger">Inactive</span>{% endif %}
                        </td>
                        <td>
                            <a href="{% url 'admin_toggle_officer' o.officer_id %}" class="btn btn-sm btn-outline-secondary">
                                {% if o.is_active %}Deactivate{% else %}Activate{% endif %}
                            </a>
                        </td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="6" class="text-center py-4">No officers found.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}"""

admin_add_officer_html = """{% extends 'myapp/admin_base.html' %}
{% block title %}Add Insurance Officer{% endblock %}
{% block admin_content %}
<div class="container-fluid p-4">
    <h3 class="fw-bold mb-4">Add New Insurance Officer</h3>
    
    <div class="card shadow-sm border-0">
        <div class="card-body p-4">
            <form method="post">
                {% csrf_token %}
                {{ form.as_p }}
                <button type="submit" class="btn btn-primary mt-3 px-4">Create Officer</button>
                <a href="{% url 'admin_officers' %}" class="btn btn-secondary mt-3">Cancel</a>
            </form>
        </div>
    </div>
</div>
{% endblock %}"""

admin_insurance_dashboard_html = """{% extends 'myapp/admin_base.html' %}
{% block title %}Insurance Overview{% endblock %}
{% block admin_content %}
<div class="container-fluid p-4">
    <h2 class="fw-bold text-success mb-4"><i class="bi bi-shield-check"></i> Admin Insurance Overview</h2>
    
    <div class="row g-4 mb-5">
        <div class="col-md-3"><div class="card shadow-sm p-4 text-center"><h5>Total Policies</h5><h2 class="text-primary">{{ policies.count }}</h2></div></div>
        <div class="col-md-3"><div class="card shadow-sm p-4 text-center"><h5>Enrolled Farmers</h5><h2 class="text-success">{{ enrollments.count }}</h2></div></div>
        <div class="col-md-3"><div class="card shadow-sm p-4 text-center"><h5>Total Claims</h5><h2 class="text-warning">{{ claims.count }}</h2></div></div>
        <div class="col-md-3"><div class="card shadow-sm p-4 text-center"><h5>Settled Claims</h5><h2 class="text-info">{{ settlements.count }}</h2></div></div>
    </div>
    
    <h4 class="fw-bold mb-3">Recent Claims Overview</h4>
    <div class="card shadow-sm border-0 mb-5">
        <div class="table-responsive">
            <table class="table table-hover mb-0">
                <thead class="table-light">
                    <tr>
                        <th>Claim ID</th><th>Farmer</th><th>Loss Est.</th><th>Status</th><th>Reviewer</th>
                    </tr>
                </thead>
                <tbody>
                    {% for c in claims|slice:":10" %}
                    <tr>
                        <td>{{ c.claim_id }}</td>
                        <td>{{ c.enrollment.farmer.full_name }}</td>
                        <td>₹{{ c.estimated_financial_loss }}</td>
                        <td><span class="badge bg-secondary">{{ c.status }}</span></td>
                        <td>{% if c.reviewed_by %}{{ c.reviewed_by.full_name }}{% else %}-{% endif %}</td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="5" class="text-center py-3">No claims found.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}"""

with open(os.path.join(templates_dir, 'admin_officers.html'), 'w', encoding='utf-8') as f:
    f.write(admin_officers_html)
with open(os.path.join(templates_dir, 'admin_add_officer.html'), 'w', encoding='utf-8') as f:
    f.write(admin_add_officer_html)
with open(os.path.join(templates_dir, 'admin_insurance_dashboard.html'), 'w', encoding='utf-8') as f:
    f.write(admin_insurance_dashboard_html)
    
print("Admin views, URLs and templates successfully updated.")
