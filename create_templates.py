import os

templates_dir = r"c:\Users\Asus\python-project\MCA_Project\myapp\templates\myapp"
os.makedirs(templates_dir, exist_ok=True)

templates = {
    "officer_login.html": """{% extends 'myapp/base.html' %}
{% block title %}Insurance Officer Login{% endblock %}
{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-5">
            <div class="card border-0 shadow-sm rounded-4">
                <div class="card-body p-5">
                    <div class="text-center mb-4">
                        <i class="bi bi-shield-check text-primary" style="font-size: 3rem;"></i>
                        <h4 class="fw-bold mt-2">Insurance Officer Login</h4>
                        <p class="text-muted">Manage agricultural insurance policies</p>
                    </div>
                    {% if error_message %}
                        <div class="alert alert-danger">{{ error_message }}</div>
                    {% endif %}
                    <form method="post">
                        {% csrf_token %}
                        <div class="mb-3">
                            {{ form.email.label_tag }}
                            {{ form.email }}
                        </div>
                        <div class="mb-4">
                            {{ form.password.label_tag }}
                            {{ form.password }}
                        </div>
                        <button type="submit" class="btn btn-primary w-100 py-2 fw-bold rounded-pill">Login</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""",

    "officer_dashboard.html": """{% extends 'myapp/erp_base.html' %}
{% block title %}Officer Dashboard{% endblock %}
{% block erp_content %}
<div class="container-fluid px-0">
    <div class="glass-card p-4 mb-4 text-white" style="background: linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%);">
        <h2 class="fw-bold mb-1">Insurance Officer Dashboard</h2>
        <p class="mb-0 text-white-50">Welcome, {{ officer.full_name }}!</p>
    </div>
    <div class="row g-4">
        <div class="col-md-3"><div class="card shadow-sm p-4 text-center"><h5>Total Policies</h5><h2 class="text-primary">{{ total_policies }}</h2></div></div>
        <div class="col-md-3"><div class="card shadow-sm p-4 text-center"><h5>Active Policies</h5><h2 class="text-success">{{ active_policies }}</h2></div></div>
        <div class="col-md-3"><div class="card shadow-sm p-4 text-center"><h5>Enrolled Farmers</h5><h2 class="text-info">{{ enrolled_farmers }}</h2></div></div>
        <div class="col-md-3"><div class="card shadow-sm p-4 text-center"><h5>Premium Payments</h5><h2 class="text-warning">{{ premium_payments }}</h2></div></div>
        <div class="col-md-3"><div class="card shadow-sm p-4 text-center"><h5>Pending Claims</h5><h2 class="text-danger">{{ pending_claims }}</h2></div></div>
        <div class="col-md-3"><div class="card shadow-sm p-4 text-center"><h5>Approved Claims</h5><h2 class="text-success">{{ approved_claims }}</h2></div></div>
        <div class="col-md-3"><div class="card shadow-sm p-4 text-center"><h5>Rejected Claims</h5><h2 class="text-secondary">{{ rejected_claims }}</h2></div></div>
        <div class="col-md-3"><div class="card shadow-sm p-4 text-center"><h5>Settled Claims</h5><h2 class="text-primary">{{ settled_claims }}</h2></div></div>
    </div>
</div>
{% endblock %}
""",

    "officer_policies.html": """{% extends 'myapp/erp_base.html' %}
{% block title %}Manage Policies{% endblock %}
{% block erp_content %}
<div class="container-fluid px-0">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h3 class="fw-bold mb-0">Insurance Policies</h3>
        <a href="{% url 'officer_add_policy' %}" class="btn btn-primary"><i class="bi bi-plus-circle"></i> Add Policy</a>
    </div>
    <div class="card shadow-sm border-0">
        <div class="table-responsive">
            <table class="table table-hover mb-0">
                <thead class="table-light">
                    <tr>
                        <th>ID</th><th>Name</th><th>Crop</th><th>Max Coverage</th><th>Premium</th><th>Status</th><th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for policy in policies %}
                    <tr>
                        <td>{{ policy.policy_id }}</td>
                        <td>{{ policy.name }}</td>
                        <td>{{ policy.eligible_crop }}</td>
                        <td>₹{{ policy.max_coverage_amount }}</td>
                        <td>₹{{ policy.premium_amount }} ({{ policy.get_payment_frequency_display }})</td>
                        <td>
                            {% if policy.is_active %}<span class="badge bg-success">Active</span>{% else %}<span class="badge bg-danger">Inactive</span>{% endif %}
                        </td>
                        <td>
                            <a href="{% url 'officer_edit_policy' policy.policy_id %}" class="btn btn-sm btn-outline-primary">Edit</a>
                            <a href="{% url 'officer_toggle_policy' policy.policy_id %}" class="btn btn-sm btn-outline-secondary">
                                {% if policy.is_active %}Deactivate{% else %}Activate{% endif %}
                            </a>
                        </td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="7" class="text-center py-4">No policies found.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
""",

    "officer_policy_form.html": """{% extends 'myapp/erp_base.html' %}
{% block title %}{{ title }}{% endblock %}
{% block erp_content %}
<div class="container-fluid px-0">
    <h3 class="fw-bold mb-4">{{ title }}</h3>
    <div class="card shadow-sm border-0">
        <div class="card-body p-4">
            <form method="post">
                {% csrf_token %}
                {{ form.as_p }}
                <button type="submit" class="btn btn-primary mt-3">Save Policy</button>
                <a href="{% url 'officer_policies' %}" class="btn btn-secondary mt-3">Cancel</a>
            </form>
        </div>
    </div>
</div>
{% endblock %}
""",

    "officer_enrollments.html": """{% extends 'myapp/erp_base.html' %}
{% block title %}Enrolled Farmers{% endblock %}
{% block erp_content %}
<div class="container-fluid px-0">
    <h3 class="fw-bold mb-4">Enrolled Farmers</h3>
    <div class="card shadow-sm border-0">
        <div class="table-responsive">
            <table class="table table-hover mb-0">
                <thead class="table-light">
                    <tr>
                        <th>Enrollment ID</th><th>Farmer</th><th>Policy</th><th>Crop</th><th>Area</th><th>Start Date</th><th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for enc in enrollments %}
                    <tr>
                        <td>{{ enc.enrollment_id }}</td>
                        <td>{{ enc.farmer.full_name }}</td>
                        <td>{{ enc.policy.name }}</td>
                        <td>{{ enc.crop_name }}</td>
                        <td>{{ enc.farm_area }} acres</td>
                        <td>{{ enc.coverage_period_start }}</td>
                        <td>{{ enc.get_status_display }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
""",

    "officer_premiums.html": """{% extends 'myapp/erp_base.html' %}
{% block title %}Premium Payments{% endblock %}
{% block erp_content %}
<div class="container-fluid px-0">
    <h3 class="fw-bold mb-4">Premium Payments</h3>
    <div class="card shadow-sm border-0">
        <div class="table-responsive">
            <table class="table table-hover mb-0">
                <thead class="table-light">
                    <tr>
                        <th>Payment ID</th><th>Enrollment</th><th>Farmer</th><th>Amount</th><th>Date</th><th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for p in payments %}
                    <tr>
                        <td>{{ p.payment_id }}</td>
                        <td>{{ p.enrollment.enrollment_id }}</td>
                        <td>{{ p.enrollment.farmer.full_name }}</td>
                        <td>₹{{ p.amount }}</td>
                        <td>{{ p.payment_date|date:"d M Y" }}</td>
                        <td><span class="badge bg-success">{{ p.status }}</span></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
""",

    "officer_claims.html": """{% extends 'myapp/erp_base.html' %}
{% block title %}Insurance Claims{% endblock %}
{% block erp_content %}
<div class="container-fluid px-0">
    <h3 class="fw-bold mb-4">Insurance Claims</h3>
    <div class="card shadow-sm border-0">
        <div class="table-responsive">
            <table class="table table-hover mb-0">
                <thead class="table-light">
                    <tr>
                        <th>Claim ID</th><th>Farmer</th><th>Policy</th><th>Incident</th><th>Loss Est.</th><th>Status</th><th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for c in claims %}
                    <tr>
                        <td>{{ c.claim_id }}</td>
                        <td>{{ c.enrollment.farmer.full_name }}</td>
                        <td>{{ c.enrollment.policy.name }}</td>
                        <td>{{ c.incident_type }} ({{ c.incident_date }})</td>
                        <td>₹{{ c.estimated_financial_loss }}</td>
                        <td>
                            <span class="badge {% if c.status == 'SUBMITTED' %}bg-warning{% elif c.status == 'APPROVED' %}bg-success{% elif c.status == 'REJECTED' %}bg-danger{% else %}bg-info{% endif %}">{{ c.status }}</span>
                        </td>
                        <td>
                            <a href="{% url 'officer_claim_detail' c.claim_id %}" class="btn btn-sm btn-outline-primary">Review</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
""",

    "officer_claim_detail.html": """{% extends 'myapp/erp_base.html' %}
{% block title %}Review Claim {{ claim.claim_id }}{% endblock %}
{% block erp_content %}
<div class="container-fluid px-0">
    <h3 class="fw-bold mb-4">Review Claim: {{ claim.claim_id }}</h3>
    <div class="row">
        <div class="col-md-6">
            <div class="card shadow-sm border-0 mb-4">
                <div class="card-header bg-white"><h5 class="mb-0">Claim Details</h5></div>
                <div class="card-body">
                    <p><strong>Farmer:</strong> {{ claim.enrollment.farmer.full_name }}</p>
                    <p><strong>Policy:</strong> {{ claim.enrollment.policy.name }}</p>
                    <p><strong>Incident Type:</strong> {{ claim.incident_type }}</p>
                    <p><strong>Incident Date:</strong> {{ claim.incident_date }}</p>
                    <p><strong>Description:</strong> {{ claim.damage_description }}</p>
                    <p><strong>Affected Area:</strong> {{ claim.affected_farm_area }} acres</p>
                    <p><strong>Est. Loss:</strong> ₹{{ claim.estimated_financial_loss }}</p>
                    {% if claim.evidence_file %}
                    <p><strong>Evidence:</strong> <a href="{{ claim.evidence_file.url }}" target="_blank">View File</a></p>
                    {% endif %}
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card shadow-sm border-0">
                <div class="card-header bg-white"><h5 class="mb-0">Officer Review</h5></div>
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        {{ form.as_p }}
                        <button type="submit" class="btn btn-primary w-100 mt-2">Submit Decision</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""",

    "officer_settlements.html": """{% extends 'myapp/erp_base.html' %}
{% block title %}Claim Settlements{% endblock %}
{% block erp_content %}
<div class="container-fluid px-0">
    <h3 class="fw-bold mb-4">Pending Settlements</h3>
    <div class="card shadow-sm border-0 mb-5">
        <div class="table-responsive">
            <table class="table table-hover mb-0">
                <thead class="table-light">
                    <tr>
                        <th>Claim ID</th><th>Farmer</th><th>Approved Amount</th><th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {% for c in pending_claims %}
                    <tr>
                        <td>{{ c.claim_id }}</td>
                        <td>{{ c.enrollment.farmer.full_name }}</td>
                        <td>₹{{ c.approved_amount }}</td>
                        <td>
                            <form method="post" action="{% url 'officer_settle_claim' c.claim_id %}">
                                {% csrf_token %}
                                <button type="submit" class="btn btn-sm btn-success">Settle Claim</button>
                            </form>
                        </td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="4" class="text-center py-3">No pending settlements.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    
    <h3 class="fw-bold mb-4">Settlement History</h3>
    <div class="card shadow-sm border-0">
        <div class="table-responsive">
            <table class="table table-hover mb-0">
                <thead class="table-light">
                    <tr>
                        <th>Settlement ID</th><th>Claim ID</th><th>Amount</th><th>Date</th><th>Method</th>
                    </tr>
                </thead>
                <tbody>
                    {% for s in settlements %}
                    <tr>
                        <td>{{ s.settlement_id }}</td>
                        <td>{{ s.claim.claim_id }}</td>
                        <td>₹{{ s.amount }}</td>
                        <td>{{ s.settlement_date }}</td>
                        <td>{{ s.payment_method }} {% if s.is_simulated %}(Simulated){% endif %}</td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="5" class="text-center py-3">No settlements found.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
""",

    "farmer_insurance_list.html": """{% extends 'myapp/erp_base.html' %}
{% block title %}Available Insurance Policies{% endblock %}
{% block erp_content %}
<div class="container-fluid px-0">
    <h3 class="fw-bold mb-4">Available Agricultural Insurance</h3>
    <div class="row g-4">
        {% for policy in policies %}
        <div class="col-md-6 col-lg-4">
            <div class="card shadow-sm border-0 h-100 rounded-4">
                <div class="card-body p-4">
                    <h5 class="fw-bold">{{ policy.name }}</h5>
                    <p class="text-muted small mb-3">Crop: {{ policy.eligible_crop }}</p>
                    <p>{{ policy.description|truncatechars:100 }}</p>
                    <div class="p-3 bg-light rounded-3 mb-3">
                        <div class="d-flex justify-content-between mb-2"><span class="small">Max Coverage:</span><span class="fw-bold text-success">₹{{ policy.max_coverage_amount }}</span></div>
                        <div class="d-flex justify-content-between"><span class="small">Premium:</span><span class="fw-bold">₹{{ policy.premium_amount }} ({{ policy.get_payment_frequency_display }})</span></div>
                    </div>
                    <a href="{% url 'farmer_buy_insurance' policy.policy_id %}" class="btn btn-outline-success w-100 rounded-pill">View & Buy</a>
                </div>
            </div>
        </div>
        {% empty %}
        <div class="col-12"><div class="alert alert-info">No active insurance policies are currently available.</div></div>
        {% endfor %}
    </div>
</div>
{% endblock %}
""",

    "farmer_buy_insurance.html": """{% extends 'myapp/erp_base.html' %}
{% block title %}Buy Insurance{% endblock %}
{% block erp_content %}
<div class="container-fluid px-0">
    <div class="row">
        <div class="col-md-5">
            <h3 class="fw-bold mb-4">Policy Details</h3>
            <div class="card shadow-sm border-0 p-4">
                <h5 class="fw-bold">{{ policy.name }}</h5>
                <p><strong>Eligible Crop:</strong> {{ policy.eligible_crop }}</p>
                <p><strong>Covered Risks:</strong> {{ policy.covered_risks }}</p>
                <p><strong>Max Coverage:</strong> ₹{{ policy.max_coverage_amount }}</p>
                <p><strong>Premium:</strong> ₹{{ policy.premium_amount }} ({{ policy.get_payment_frequency_display }})</p>
                <p><strong>Start Date:</strong> {{ policy.coverage_start_date }}</p>
                <p><strong>End Date:</strong> {{ policy.coverage_end_date }}</p>
                <hr>
                <p class="small text-muted">{{ policy.terms_and_conditions }}</p>
            </div>
        </div>
        <div class="col-md-7">
            <h3 class="fw-bold mb-4">Enrollment Form</h3>
            <div class="card shadow-sm border-0 p-4">
                <form method="post">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <div class="form-check mb-4 mt-3">
                        <input class="form-check-input" type="checkbox" name="accepted_terms" id="accepted_terms">
                        <label class="form-check-label" for="accepted_terms">I accept the terms and conditions</label>
                    </div>
                    <button type="submit" class="btn btn-success w-100 rounded-pill">Enroll & Pay</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""",

    "farmer_my_policies.html": """{% extends 'myapp/erp_base.html' %}
{% block title %}My Active Policies{% endblock %}
{% block erp_content %}
<div class="container-fluid px-0">
    <h3 class="fw-bold mb-4">My Insurance Policies</h3>
    <div class="row g-4">
        {% for enc in enrollments %}
        <div class="col-md-6 col-lg-6">
            <div class="card shadow-sm border-0 h-100 rounded-4">
                <div class="card-body p-4">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5 class="fw-bold mb-0">{{ enc.policy.name }}</h5>
                        <span class="badge {% if enc.status == 'ACTIVE' %}bg-success{% elif enc.status == 'PENDING_PAYMENT' %}bg-warning{% else %}bg-secondary{% endif %}">{{ enc.get_status_display }}</span>
                    </div>
                    <p class="mb-1"><strong>Enrollment ID:</strong> {{ enc.enrollment_id }}</p>
                    <p class="mb-1"><strong>Crop:</strong> {{ enc.crop_name }} ({{ enc.farm_area }} acres)</p>
                    <p class="mb-1"><strong>Coverage Period:</strong> {{ enc.coverage_period_start }} to {{ enc.coverage_period_end }}</p>
                    <div class="p-3 bg-light rounded-3 mt-3">
                        <div class="d-flex justify-content-between mb-2"><span class="small">Coverage:</span><span class="fw-bold text-success">₹{{ enc.policy.max_coverage_amount }}</span></div>
                        <div class="d-flex justify-content-between"><span class="small">Premium:</span><span class="fw-bold">₹{{ enc.premium_amount_due }} ({{ enc.payment_frequency }})</span></div>
                    </div>
                    {% if enc.status == 'PENDING_PAYMENT' %}
                    <div class="mt-3 text-center">
                        <a href="{% url 'farmer_pay_premium' enc.enrollment_id %}" class="btn btn-warning w-100">Pay Premium Now</a>
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>
        {% empty %}
        <div class="col-12"><div class="alert alert-info">You have not enrolled in any policies yet.</div></div>
        {% endfor %}
    </div>
</div>
{% endblock %}
""",

    "farmer_pay_premium.html": """{% extends 'myapp/erp_base.html' %}
{% block title %}Pay Premium{% endblock %}
{% block erp_content %}
<div class="container-fluid px-0">
    <h3 class="fw-bold mb-4">Pay Premium</h3>
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card shadow-sm border-0 p-4">
                <h5 class="mb-3">Policy: {{ enrollment.policy.name }}</h5>
                <div class="d-flex justify-content-between mb-2"><span>Amount Due:</span><span class="fw-bold">₹{{ enrollment.premium_amount_due }}</span></div>
                <div class="d-flex justify-content-between mb-4"><span>Wallet Balance:</span><span class="fw-bold {% if wallet.balance < enrollment.premium_amount_due %}text-danger{% else %}text-success{% endif %}">₹{{ wallet.balance }}</span></div>
                
                <form method="post">
                    {% csrf_token %}
                    {% if wallet.balance >= enrollment.premium_amount_due %}
                        <button type="submit" class="btn btn-success w-100 rounded-pill">Pay from Wallet (Simulated)</button>
                    {% else %}
                        <button type="button" class="btn btn-secondary w-100 rounded-pill" disabled>Insufficient Balance</button>
                        <p class="text-danger small text-center mt-2">Please top up your wallet to pay.</p>
                    {% endif %}
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""",

    "farmer_premium_history.html": """{% extends 'myapp/erp_base.html' %}
{% block title %}Premium History{% endblock %}
{% block erp_content %}
<div class="container-fluid px-0">
    <h3 class="fw-bold mb-4">Premium Payment History</h3>
    <div class="card shadow-sm border-0">
        <div class="table-responsive">
            <table class="table table-hover mb-0">
                <thead class="table-light">
                    <tr>
                        <th>Payment ID</th><th>Policy</th><th>Amount</th><th>Date</th><th>Method</th><th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for p in payments %}
                    <tr>
                        <td>{{ p.payment_id }}</td>
                        <td>{{ p.enrollment.policy.name }}</td>
                        <td>₹{{ p.amount }}</td>
                        <td>{{ p.payment_date|date:"d M Y, h:i A" }}</td>
                        <td>{{ p.payment_method }}</td>
                        <td><span class="badge bg-success">{{ p.status }}</span></td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="6" class="text-center py-4">No premium payments found.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
""",

    "farmer_apply_claim.html": """{% extends 'myapp/erp_base.html' %}
{% block title %}Apply for Claim{% endblock %}
{% block erp_content %}
<div class="container-fluid px-0">
    <h3 class="fw-bold mb-4">Apply for Crop-Loss Claim</h3>
    <div class="card shadow-sm border-0 p-4">
        <form method="post" enctype="multipart/form-data">
            {% csrf_token %}
            <div class="mb-3">
                <label class="form-label">Select Active Policy</label>
                <select name="enrollment_id" class="form-select" required>
                    <option value="">-- Select Policy --</option>
                    {% for e in enrollments %}
                        <option value="{{ e.enrollment_id }}">{{ e.policy.name }} ({{ e.crop_name }})</option>
                    {% endfor %}
                </select>
            </div>
            {{ form.as_p }}
            <button type="submit" class="btn btn-success mt-3 rounded-pill px-4">Submit Claim</button>
        </form>
    </div>
</div>
{% endblock %}
""",

    "farmer_my_claims.html": """{% extends 'myapp/erp_base.html' %}
{% block title %}My Claims{% endblock %}
{% block erp_content %}
<div class="container-fluid px-0">
    <h3 class="fw-bold mb-4">My Insurance Claims</h3>
    <div class="row g-4">
        {% for c in claims %}
        <div class="col-md-6">
            <div class="card shadow-sm border-0 h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between mb-2">
                        <h5 class="fw-bold">{{ c.claim_id }}</h5>
                        <span class="badge {% if c.status == 'APPROVED' or c.status == 'PAID' %}bg-success{% elif c.status == 'REJECTED' %}bg-danger{% else %}bg-warning{% endif %}">{{ c.get_status_display }}</span>
                    </div>
                    <p class="mb-1"><strong>Policy:</strong> {{ c.enrollment.policy.name }}</p>
                    <p class="mb-1"><strong>Incident:</strong> {{ c.incident_type }} on {{ c.incident_date }}</p>
                    <p class="mb-1"><strong>Est. Loss:</strong> ₹{{ c.estimated_financial_loss }}</p>
                    {% if c.approved_amount %}
                        <p class="mb-1 text-success"><strong>Approved Amount:</strong> ₹{{ c.approved_amount }}</p>
                    {% endif %}
                    {% if c.rejection_reason %}
                        <p class="mb-1 text-danger"><strong>Reason:</strong> {{ c.rejection_reason }}</p>
                    {% endif %}
                </div>
            </div>
        </div>
        {% empty %}
        <div class="col-12"><div class="alert alert-info">You have not submitted any claims.</div></div>
        {% endfor %}
    </div>
</div>
{% endblock %}
"""
}

for filename, content in templates.items():
    file_path = os.path.join(templates_dir, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
print("All templates created successfully.")
