from django import forms
from django.core.validators import MinValueValidator
from .models import Farmer, Customer, Worker, Delivery, MarketSettings, Product, BargainingBid, WorkerRequest, WorkerWageOffer, WorkerTask, WalletTransaction, WorkerSalarySettlement, AdminSupply, SupplyPurchase

class RegistrationValidationMixin:
    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Phone number must contain exactly 10 digits.")
        return phone

    def clean_full_name(self):
        name = self.cleaned_data.get('full_name', '')
        if name is not None:
            name = name.strip()
        if not name:
            raise forms.ValidationError("This field is required.")
        if name.isdigit():
            raise forms.ValidationError("Name cannot contain only numbers.")
        return name

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and age <= 0:
            raise forms.ValidationError("Age must be a valid positive number.")
        return age

    def clean_address(self):
        address = self.cleaned_data.get('address', '')
        if address is not None:
            address = address.strip()
        if not address:
            raise forms.ValidationError("This field is required.")
        return address

    def clean_place(self):
        place = self.cleaned_data.get('place', '')
        if place is not None:
            place = place.strip()
        if not place:
            raise forms.ValidationError("This field is required.")
        return place

class FarmerRegistrationForm(RegistrationValidationMixin, forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        }),
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        }),
        label='Confirm Password'
    )

    class Meta:
        model = Farmer
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age', 'min': '18', 'max': '120'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Town / Village'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'pattern': '[0-9]{10}', 'title': 'Phone number must contain exactly 10 digits.'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Farmer.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class FarmerLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter registered email'
        }),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }),
        label='Password'
    )


class FarmerProfileForm(RegistrationValidationMixin, forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '18', 'max': '120'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]{10}', 'title': 'Phone number must contain exactly 10 digits.'}),
        }


class AdminLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter admin email'
        }),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter admin password'
        }),
        label='Password'
    )


# ====================================================
# CUSTOMER FORMS
# ====================================================

class CustomerRegistrationForm(RegistrationValidationMixin, forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        }),
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        }),
        label='Confirm Password'
    )

    class Meta:
        model = Customer
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age', 'min': '18', 'max': '120'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Town / Village'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'pattern': '[0-9]{10}', 'title': 'Phone number must contain exactly 10 digits.'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Customer.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class CustomerLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter registered email'
        }),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }),
        label='Password'
    )


class CustomerProfileForm(RegistrationValidationMixin, forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '18', 'max': '120'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]{10}', 'title': 'Phone number must contain exactly 10 digits.'}),
        }


# ====================================================
# WORKER FORMS
# ====================================================

class WorkerRegistrationForm(RegistrationValidationMixin, forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        }),
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        }),
        label='Confirm Password'
    )

    class Meta:
        model = Worker
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age', 'min': '18', 'max': '120'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Town / Village'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'pattern': '[0-9]{10}', 'title': 'Phone number must contain exactly 10 digits.'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Worker.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class WorkerLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter registered email'
        }),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }),
        label='Password'
    )


class WorkerProfileForm(RegistrationValidationMixin, forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '18', 'max': '120'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]{10}', 'title': 'Phone number must contain exactly 10 digits.'}),
        }


# ====================================================
# DELIVERY PERSON FORMS
# ====================================================

class AdminDeliveryForm(RegistrationValidationMixin, forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter temporary password'
        }),
        label='Password',
        required=False
    )
    
    class Meta:
        model = Delivery
        fields = ['full_name', 'phone', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'pattern': '[0-9]{10}', 'title': 'Phone number must contain exactly 10 digits.'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Ensure email is unique
        if email:
            qs = Delivery.objects.filter(email=email)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("An account with this email address already exists.")
        return email


class DeliveryRegistrationForm(RegistrationValidationMixin, forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        }),
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        }),
        label='Confirm Password'
    )

    class Meta:
        model = Delivery
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age', 'min': '18', 'max': '120'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Town / Village'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'pattern': '[0-9]{10}', 'title': 'Phone number must contain exactly 10 digits.'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Delivery.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class DeliveryLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter registered email'
        }),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }),
        label='Password'
    )


class DeliveryProfileForm(RegistrationValidationMixin, forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '18', 'max': '120'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]{10}', 'title': 'Phone number must contain exactly 10 digits.'}),
        }


# ====================================================
# MARKETPLACE MODULE FORMS
# ====================================================

class MarketSettingsForm(forms.ModelForm):
    class Meta:
        model = MarketSettings
        fields = ['status', 'market_date', 'opening_time', 'closing_time']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select fw-bold'}),
            'market_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'opening_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'description', 'quantity', 'unit', 'price_per_unit', 'image']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Organic Tomatoes'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Vegetables, Fruits, Dairy Products'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detailed product description...'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '1', 'placeholder': 'Quantity available'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'price_per_unit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '1', 'placeholder': 'Starting Price per Unit (₹)'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': '.png, .jpg, .jpeg, image/png, image/jpeg'}),
        }
        error_messages = {
            'image': {
                'invalid_image': "Please upload an image in JPG, JPEG, or PNG format.",
            }
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            return image

        if hasattr(image, 'name'):
            import os
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise forms.ValidationError("Please upload an image in JPG, JPEG, or PNG format.")
            
            try:
                from PIL import Image
                img = Image.open(image)
                img.verify()
                if img.format.upper() not in ['JPEG', 'PNG']:
                    raise forms.ValidationError("Please upload an image in JPG, JPEG, or PNG format.")
                image.seek(0)
            except Exception:
                raise forms.ValidationError("Please upload an image in JPG, JPEG, or PNG format.")
                
        return image

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 1:
            raise forms.ValidationError("Enter 1 or greater value.")
        return quantity

    def clean_price_per_unit(self):
        price = self.cleaned_data.get('price_per_unit')
        if price is not None and price < 1:
            raise forms.ValidationError("Enter 1 or greater value.")
        return price


class BidForm(forms.ModelForm):
    class Meta:
        model = BargainingBid
        fields = ['bid_price_per_unit']
        widgets = {
            'bid_price_per_unit': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'step': '0.01', 'min': '0.01', 'placeholder': 'Enter your bid price per unit (₹)'}),
        }

    def clean_bid_price_per_unit(self):
        bid_price = self.cleaned_data.get('bid_price_per_unit')
        if bid_price is not None and bid_price <= 0:
            raise forms.ValidationError("Bid amount must be greater than 0.")
        return bid_price

# ====================================================
# WORKER MANAGEMENT & PAYMENT FORMS
# ====================================================

class AdminWorkerForm(RegistrationValidationMixin, forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter temporary password'
        }),
        label='Password',
        required=True
    )
    
    class Meta:
        model = Worker
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone', 'email', 'status']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age', 'min': '18', 'max': '120'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Town / Village'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = Worker.objects.filter(email=email)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("An account with this email address already exists.")
        return email


class WorkerRequestForm(forms.ModelForm):
    class Meta:
        model = WorkerRequest
        fields = ['num_workers', 'work_description', 'location', 'start_date', 'duration_days', 'requested_wage']
        widgets = {
            'num_workers': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'Number of workers needed'}),
            'work_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe the work (e.g. Tomato Planting)'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Work location'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'Duration in days'}),
            'requested_wage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '1', 'placeholder': 'Expected Daily Wage per Worker (₹)'}),
        }

    def clean_num_workers(self):
        val = self.cleaned_data.get('num_workers')
        if val is not None and val <= 0:
            raise forms.ValidationError("Quantity must be greater than 0.")
        return val

    def clean_duration_days(self):
        val = self.cleaned_data.get('duration_days')
        if val is not None and val <= 0:
            raise forms.ValidationError("Duration must be greater than 0.")
        return val

    def clean_requested_wage(self):
        val = self.cleaned_data.get('requested_wage')
        if val is not None and val <= 0:
            raise forms.ValidationError("Amount must be greater than 0.")
        return val


class WorkerWageOfferForm(forms.ModelForm):
    class Meta:
        model = WorkerWageOffer
        fields = ['amount_per_worker_per_day', 'message']
        widgets = {
            'amount_per_worker_per_day': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '1', 'placeholder': 'Offer amount (₹)'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional note/message'}),
        }

    def clean_amount_per_worker_per_day(self):
        val = self.cleaned_data.get('amount_per_worker_per_day')
        if val is not None and val <= 0:
            raise forms.ValidationError("Amount must be greater than 0.")
        return val


class WorkerTaskForm(forms.ModelForm):
    class Meta:
        model = WorkerTask
        fields = ['work_description', 'location', 'start_date', 'duration_days']
        widgets = {
            'work_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Task Details'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Work location'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'Duration in days'}),
        }

    def clean_duration_days(self):
        val = self.cleaned_data.get('duration_days')
        if val is not None and val <= 0:
            raise forms.ValidationError("Duration must be greater than 0.")
        return val


class AdminSupplyForm(forms.ModelForm):
    class Meta:
        model = AdminSupply
        fields = ['supply_name', 'category', 'description', 'price', 'unit', 'available_quantity', 'image', 'status']
        widgets = {
            'supply_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Tomato Seeds'}),
            'category': forms.Select(choices=[
                ('Seeds', 'Seeds'),
                ('Plants', 'Plants'),
                ('Fertilizers', 'Fertilizers'),
                ('Equipment', 'Equipment'),
                ('Other', 'Other'),
            ], attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Supply description...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Packet, Kg, Bottle'}),
            'available_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': '.png, .jpg, .jpeg, image/png, image/jpeg'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        error_messages = {
            'image': {
                'invalid_image': "Please upload an image in JPG, JPEG, or PNG format.",
            }
        }

    def clean_price(self):
        val = self.cleaned_data.get('price')
        if val is not None and val <= 0:
            raise forms.ValidationError("Price must be greater than 0.")
        return val

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            return image

        if hasattr(image, 'name'):
            import os
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise forms.ValidationError("Please upload an image in JPG, JPEG, or PNG format.")
            
            try:
                from PIL import Image
                img = Image.open(image)
                img.verify()
                if img.format.upper() not in ['JPEG', 'PNG']:
                    raise forms.ValidationError("Please upload an image in JPG, JPEG, or PNG format.")
                image.seek(0)
            except Exception:
                raise forms.ValidationError("Please upload an image in JPG, JPEG, or PNG format.")
                
        return image

# ====================================================
# AGRICULTURAL INSURANCE FORMS
# ====================================================
from decimal import Decimal
from django.utils import timezone
from .models import InsurancePolicy, FarmerPolicyEnrollment, InsuranceClaim, InsuranceOfficer

class OfficerLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        label='Email Address'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        label='Password'
    )

class InsurancePolicyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['premium_amount'].initial = Decimal('2000.00')
            self.fields['coverage_duration'].initial = '1 Year'
            self.fields['payment_frequency'].initial = 'YEARLY'
            self.fields['claim_reporting_deadline_days'].initial = 30

    class Meta:
        model = InsurancePolicy
        fields = ['name', 'description', 'eligible_crop', 'covered_risks', 'max_coverage_amount', 
                  'premium_amount', 'coverage_duration', 'payment_frequency', 'coverage_start_date', 'coverage_end_date',
                  'claim_reporting_deadline_days', 'terms_and_conditions', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Tomato Crop Protection Policy'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'eligible_crop': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Tomato'}),
            'covered_risks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'e.g. Flood, Heavy Rainfall, Inundation'}),
            'max_coverage_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'e.g. 50000.00'}),
            'premium_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '2000.00'}),
            'coverage_duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1 Year'}),
            'payment_frequency': forms.Select(attrs={'class': 'form-select'}),
            'coverage_start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'coverage_end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'claim_reporting_deadline_days': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'terms_and_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('coverage_start_date')
        end = cleaned_data.get('coverage_end_date')
        max_cov = cleaned_data.get('max_coverage_amount')
        prem = cleaned_data.get('premium_amount')

        if start and end and end <= start:
            self.add_error('coverage_end_date', "Coverage end date must be after coverage start date.")
        if max_cov is not None and max_cov <= 0:
            self.add_error('max_coverage_amount', "Maximum coverage amount must be greater than zero.")
        if prem is not None and prem <= 0:
            self.add_error('premium_amount', "Annual premium amount must be greater than zero.")
        return cleaned_data

class FarmerPolicyEnrollmentForm(forms.ModelForm):
    class Meta:
        model = FarmerPolicyEnrollment
        fields = ['crop_name', 'farm_area', 'farm_location']
        widgets = {
            'crop_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter crop name'}),
            'farm_area': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Farm area in acres'}),
            'farm_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Farm location/address'}),
        }

    def clean_farm_area(self):
        farm_area = self.cleaned_data.get('farm_area')
        if farm_area is not None and farm_area <= 0:
            raise forms.ValidationError("Farm area must be greater than zero.")
        return farm_area

class InsuranceClaimForm(forms.ModelForm):
    class Meta:
        model = InsuranceClaim
        fields = ['incident_type', 'incident_date', 'incident_location', 'damage_description', 
                  'affected_farm_area', 'estimated_financial_loss', 'evidence_file']
        widgets = {
            'incident_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Flood / Heavy Rainfall'}),
            'incident_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'incident_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Incident location'}),
            'damage_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detailed description of crop damage'}),
            'affected_farm_area': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Acres affected'}),
            'estimated_financial_loss': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '₹ Estimated loss'}),
            'evidence_file': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_incident_date(self):
        incident_date = self.cleaned_data.get('incident_date')
        if incident_date and incident_date > timezone.now().date():
            raise forms.ValidationError("Incident date cannot be in the future.")
        return incident_date

    def clean_estimated_financial_loss(self):
        loss = self.cleaned_data.get('estimated_financial_loss')
        if loss is not None and loss <= 0:
            raise forms.ValidationError("Estimated financial loss must be greater than zero.")
        return loss

    def clean_affected_farm_area(self):
        area = self.cleaned_data.get('affected_farm_area')
        if area is not None and area <= 0:
            raise forms.ValidationError("Affected farm area must be greater than zero.")
        return area

class ClaimReviewForm(forms.ModelForm):
    class Meta:
        model = InsuranceClaim
        fields = ['status', 'officer_notes', 'rejection_reason', 'approved_amount']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'officer_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rejection_reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'approved_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class InsuranceOfficerForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter temporary password'}),
        label='Password'
    )
    class Meta:
        model = InsuranceOfficer
        fields = ['full_name', 'email', 'phone', 'is_active']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Officer Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
