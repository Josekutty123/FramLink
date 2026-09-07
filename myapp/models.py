import re
from decimal import Decimal
from django.db import models


class Farmer(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    farmer_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=191, unique=True)
    password = models.CharField(max_length=255)
    joining_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'farmer'

    def save(self, *args, **kwargs):
        if not self.farmer_id:
            max_num = 0
            existing_ids = Farmer.objects.values_list('farmer_id', flat=True)
            for fid in existing_ids:
                if fid and fid.startswith('F'):
                    match = re.search(r'\d+', fid)
                    if match:
                        num = int(match.group())
                        if num > max_num:
                            max_num = num
            self.farmer_id = f"F{max_num + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.farmer_id} - {self.full_name}"


class Admin(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=191, unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'admin'

    def __str__(self):
        return f"{self.name} ({self.email})"


class Customer(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    customer_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=191, unique=True)
    password = models.CharField(max_length=255)
    joining_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'customer'

    def save(self, *args, **kwargs):
        if not self.customer_id:
            max_num = 0
            existing_ids = Customer.objects.values_list('customer_id', flat=True)
            for cid in existing_ids:
                if cid and cid.startswith('C'):
                    match = re.search(r'\d+', cid)
                    if match:
                        num = int(match.group())
                        if num > max_num:
                            max_num = num
            self.customer_id = f"C{max_num + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_id} - {self.full_name}"


class Worker(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    worker_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=191, unique=True)
    password = models.CharField(max_length=255)
    joining_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('AVAILABLE', 'AVAILABLE'), ('ASSIGNED', 'ASSIGNED'), ('BUSY', 'BUSY')], default='AVAILABLE')

    class Meta:
        db_table = 'worker'

    def save(self, *args, **kwargs):
        if not self.worker_id:
            max_num = 0
            existing_ids = Worker.objects.values_list('worker_id', flat=True)
            for wid in existing_ids:
                if wid and wid.startswith('W'):
                    match = re.search(r'\d+', wid)
                    if match:
                        num = int(match.group())
                        if num > max_num:
                            max_num = num
            self.worker_id = f"W{max_num + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.worker_id} - {self.full_name}"


class Delivery(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    delivery_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    full_name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=191, unique=True)
    password = models.CharField(max_length=255)
    joining_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('AVAILABLE', 'AVAILABLE'), ('BUSY', 'BUSY'), ('INACTIVE', 'INACTIVE')], default='AVAILABLE')

    class Meta:
        db_table = 'delivery'

    def save(self, *args, **kwargs):
        if not self.delivery_id:
            max_num = 0
            existing_ids = Delivery.objects.values_list('delivery_id', flat=True)
            for did in existing_ids:
                if did and did.startswith('D'):
                    match = re.search(r'\d+', did)
                    if match:
                        num = int(match.group())
                        if num > max_num:
                            max_num = num
            self.delivery_id = f"D{max_num + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.delivery_id} - {self.full_name}"


# ====================================================
# MARKETPLACE MODULE MODELS
# ====================================================

class MarketSettings(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'OPEN'),
        ('CLOSED', 'CLOSED'),
    ]
    REGISTRATION_STATUS_CHOICES = [
        ('OPEN', 'OPEN'),
        ('CLOSED', 'CLOSED'),
    ]
    BARGAINING_STATUS_CHOICES = [
        ('NOT_STARTED', 'NOT_STARTED'),
        ('ACTIVE', 'ACTIVE'),
        ('STOPPED', 'STOPPED'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='CLOSED')
    product_registration_status = models.CharField(max_length=10, choices=REGISTRATION_STATUS_CHOICES, default='CLOSED')
    bargaining_status = models.CharField(max_length=15, choices=BARGAINING_STATUS_CHOICES, default='NOT_STARTED')
    market_date = models.DateField(null=True, blank=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'market_settings'

    def __str__(self):
        return f"Market Status: {self.status} (Date: {self.market_date})"

    @classmethod
    def get_settings(cls):
        settings, _ = cls.objects.get_or_create(id=1)
        return settings


class Product(models.Model):
    UNIT_CHOICES = [
        ('Kg', 'Kg'),
        ('Liter', 'Liter'),
        ('Pieces', 'Pieces'),
    ]
    STATUS_CHOICES = [
        ('AVAILABLE', 'AVAILABLE'),
        ('SOLD', 'SOLD'),
        ('UNSOLD', 'UNSOLD'),
    ]

    product_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, to_field='farmer_id', db_column='farmer_id', related_name='products')
    product_name = models.CharField(max_length=150)
    category = models.CharField(max_length=100, default='Vegetable')
    description = models.TextField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    created_at = models.DateTimeField(auto_now_add=True)

    winning_customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, to_field='customer_id', db_column='winning_customer_id', related_name='won_products')

    class Meta:
        db_table = 'product'

    def save(self, *args, **kwargs):
        if not self.product_id:
            max_num = 0
            existing_ids = Product.objects.values_list('product_id', flat=True)
            for pid in existing_ids:
                if pid and pid.startswith('P'):
                    match = re.search(r'\d+', pid)
                    if match:
                        num = int(match.group())
                        if num > max_num:
                            max_num = num
            self.product_id = f"P{max_num + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_id} - {self.product_name} ({self.farmer.full_name})"


class BargainingBid(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'ACTIVE'),
        ('ACCEPTED', 'ACCEPTED'),
        ('OUTBID', 'OUTBID'),
        ('REJECTED', 'REJECTED'),
    ]

    bid_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bids')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, to_field='customer_id', db_column='customer_id', related_name='bids')
    bid_price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_bid_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bargaining_bid'

    def save(self, *args, **kwargs):
        if not self.bid_id:
            max_num = 0
            existing_ids = BargainingBid.objects.values_list('bid_id', flat=True)
            for bid in existing_ids:
                if bid and bid.startswith('B'):
                    match = re.search(r'\d+', bid)
                    if match:
                        num = int(match.group())
                        if num > max_num:
                            max_num = num
            self.bid_id = f"B{max_num + 1}"
        if self.product and self.bid_price_per_unit:
            self.total_bid_amount = self.product.quantity * self.bid_price_per_unit
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bid_id} - {self.customer.full_name} for {self.product.product_name} @ ₹{self.bid_price_per_unit}/unit"


class FarmerWallet(models.Model):
    wallet_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, to_field='farmer_id', db_column='farmer_id', related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'farmer_wallet'

    def save(self, *args, **kwargs):
        if not self.wallet_id:
            max_num = 0
            existing_ids = FarmerWallet.objects.values_list('wallet_id', flat=True)
            for wid in existing_ids:
                if wid and wid.startswith('FW'):
                    match = re.search(r'\d+', wid)
                    if match:
                        num = int(match.group())
                        if num > max_num:
                            max_num = num
            self.wallet_id = f"FW{max_num + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Farmer Wallet ({self.farmer.farmer_id}): ₹{self.balance}"


class AdminWallet(models.Model):
    wallet_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'admin_wallet'

    def save(self, *args, **kwargs):
        if not self.wallet_id:
            max_num = 0
            existing_ids = AdminWallet.objects.values_list('wallet_id', flat=True)
            for wid in existing_ids:
                if wid and wid.startswith('AW'):
                    match = re.search(r'\d+', wid)
                    if match:
                        num = int(match.group())
                        if num > max_num:
                            max_num = num
            self.wallet_id = f"AW{max_num + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Admin Wallet ({self.admin.name}): ₹{self.balance}"


class Sale(models.Model):
    sale_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, to_field='farmer_id', db_column='farmer_id', related_name='sales')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, to_field='customer_id', db_column='customer_id', related_name='purchases')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    winning_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    farmer_share = models.DecimalField(max_digits=12, decimal_places=2)
    admin_commission = models.DecimalField(max_digits=12, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sales'

    def save(self, *args, **kwargs):
        if not self.sale_id:
            max_num = 0
            existing_ids = Sale.objects.values_list('sale_id', flat=True)
            for sid in existing_ids:
                if sid and sid.startswith('S'):
                    match = re.search(r'\d+', sid)
                    if match:
                        num = int(match.group())
                        if num > max_num:
                            max_num = num
            self.sale_id = f"S{max_num + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale {self.sale_id}: Product {self.product.product_id} - Total ₹{self.total_amount}"


class DeliveryOrder(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'PENDING'),
        ('ASSIGNED', 'ASSIGNED'),
        ('PICKED_UP', 'PICKED_UP'),
        ('OUT_FOR_DELIVERY', 'OUT_FOR_DELIVERY'),
        ('AWAITING_CUSTOMER_CONFIRMATION', 'AWAITING_CUSTOMER_CONFIRMATION'),
        ('DELIVERED', 'DELIVERED'),
    ]

    order_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='delivery_orders')
    delivery_person = models.ForeignKey(Delivery, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_deliveries')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING')
    customer_confirmation_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'delivery_order'

    def save(self, *args, **kwargs):
        if not self.order_id:
            max_num = 0
            existing_ids = DeliveryOrder.objects.values_list('order_id', flat=True)
            for oid in existing_ids:
                if oid and oid.startswith('DO'):
                    import re
                    match = re.search(r'\d+', oid)
                    if match:
                        num = int(match.group())
                        if num > max_num:
                            max_num = num
            self.order_id = f"DO{max_num + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id} - {self.status}"


# ====================================================
# WORKER MANAGEMENT & PAYMENT MODELS
# ====================================================

class WorkerRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'PENDING'),
        ('WAGE_NEGOTIATION', 'WAGE_NEGOTIATION'),
        ('WAGE_AGREED', 'WAGE_AGREED'),
        ('WORKERS_ASSIGNED', 'WORKERS_ASSIGNED'),
        ('TASK_CREATED', 'TASK_CREATED'),
        ('COMPLETED', 'COMPLETED'),
    ]

    request_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='worker_requests')
    num_workers = models.PositiveIntegerField()
    work_description = models.TextField()
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    duration_days = models.PositiveIntegerField()
    requested_wage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'worker_request'

    def save(self, *args, **kwargs):
        if not self.request_id:
            max_num = 0
            existing_ids = WorkerRequest.objects.values_list('request_id', flat=True)
            for rid in existing_ids:
                if rid and rid.startswith('WR'):
                    match = re.search(r'\d+', rid)
                    if match:
                        num = int(match.group())
                        if num > max_num:
                            max_num = num
            self.request_id = f"WR{max_num + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.request_id} - {self.farmer.full_name} ({self.num_workers} workers)"


class WorkerWageOffer(models.Model):
    OFFERED_BY_CHOICES = [
        ('FARMER', 'FARMER'),
        ('ADMIN', 'ADMIN'),
    ]
    STATUS_CHOICES = [
        ('ACTIVE', 'ACTIVE'),
        ('ACCEPTED', 'ACCEPTED'),
        ('REJECTED', 'REJECTED'),
    ]

    offer_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    worker_request = models.ForeignKey(WorkerRequest, on_delete=models.CASCADE, related_name='wage_offers')
    offered_by = models.CharField(max_length=10, choices=OFFERED_BY_CHOICES)
    amount_per_worker_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'worker_wage_offer'

    def save(self, *args, **kwargs):
        if not self.offer_id:
            max_num = 0
            existing_ids = WorkerWageOffer.objects.values_list('offer_id', flat=True)
            for oid in existing_ids:
                if oid and oid.startswith('WO'):
                    match = re.search(r'\d+', oid)
                    if match:
                        num = int(match.group())
                        if num > max_num:
                            max_num = num
            self.offer_id = f"WO{max_num + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.offer_id} - {self.offered_by}: ₹{self.amount_per_worker_per_day}"


class WorkerTask(models.Model):
    STATUS_CHOICES = [
        ('ASSIGNED', 'ASSIGNED'),
        ('IN_PROGRESS', 'IN_PROGRESS'),
        ('AWAITING_FARMER_CONFIRMATION', 'AWAITING_FARMER_CONFIRMATION'),
        ('COMPLETED', 'COMPLETED'),
    ]

    task_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='worker_tasks')
    worker_request = models.OneToOneField(WorkerRequest, on_delete=models.CASCADE, related_name='task')
    workers = models.ManyToManyField(Worker, related_name='tasks')
    work_description = models.TextField()
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    duration_days = models.PositiveIntegerField()
    daily_wage = models.DecimalField(max_digits=10, decimal_places=2)
    total_salary = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='ASSIGNED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'worker_task'

    def save(self, *args, **kwargs):
        if not self.task_id:
            max_num = 0
            existing_ids = WorkerTask.objects.values_list('task_id', flat=True)
            for tid in existing_ids:
                if tid and tid.startswith('WT'):
                    match = re.search(r'\d+', tid)
                    if match:
                        num = int(match.group())
                        if num > max_num:
                            max_num = num
            self.task_id = f"WT{max_num + 1}"
        # Ensure total salary is calculated before saving if not set
        if self.daily_wage and self.duration_days and self.pk is None: 
            pass # We calculate it in view, but keeping model clean
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.task_id} - {self.work_description}"


class WorkerSalarySettlement(models.Model):
    STATUS_CHOICES = [
        ('PAYMENT_PENDING', 'PAYMENT_PENDING'),
        ('PAID_TO_ADMIN', 'PAID_TO_ADMIN'),
        ('PAID', 'PAID'),
    ]

    settlement_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='worker_settlements')
    worker_request = models.ForeignKey(WorkerRequest, on_delete=models.SET_NULL, null=True, blank=True)
    worker_task = models.ForeignKey(WorkerTask, on_delete=models.CASCADE, related_name='settlements')
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='salary_settlements')
    duration_days = models.PositiveIntegerField()
    daily_wage = models.DecimalField(max_digits=10, decimal_places=2)
    individual_salary = models.DecimalField(max_digits=12, decimal_places=2)
    total_settlement_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PAYMENT_PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'worker_salary_settlement'

    def save(self, *args, **kwargs):
        if not self.settlement_id:
            max_num = 0
            existing_ids = WorkerSalarySettlement.objects.values_list('settlement_id', flat=True)
            for sid in existing_ids:
                if sid and sid.startswith('WSS'):
                    match = re.search(r'\d+', sid)
                    if match:
                        num = int(match.group())
                        if num > max_num:
                            max_num = num
            self.settlement_id = f"WSS{max_num + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.settlement_id} - {self.worker.full_name}: ₹{self.individual_salary}"


class WalletTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('WORKER_SALARY_PAYMENT', 'WORKER_SALARY_PAYMENT'),
        ('WALLET_TOPUP', 'WALLET_TOPUP'),
        ('WORKER_SALARY_DISBURSE', 'WORKER_SALARY_DISBURSE'),
    ]

    transaction_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='wallet_transactions', null=True, blank=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='wallet_transactions', null=True, blank=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='wallet_transactions', null=True, blank=True)
    worker_settlement = models.ForeignKey(WorkerSalarySettlement, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=30, choices=TRANSACTION_TYPES)
    prev_farmer_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    new_farmer_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    prev_admin_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    new_admin_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'wallet_transaction'

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            max_num = 0
            existing_ids = WalletTransaction.objects.values_list('transaction_id', flat=True)
            for tid in existing_ids:
                if tid and tid.startswith('TXN'):
                    match = re.search(r'\d+', tid)
                    if match:
                        num = int(match.group())
                        if num > max_num:
                            max_num = num
            self.transaction_id = f"TXN{max_num + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_id} - {self.transaction_type}: ₹{self.amount}"
