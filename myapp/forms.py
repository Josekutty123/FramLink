import os
from decimal import Decimal
from PIL import Image
from django import forms
from django.core.validators import MinValueValidator
from django.utils import timezone
from .models import (
    Farmer, Customer, Worker, Delivery, MarketSettings, Product,
    BargainingBid, WorkerRequest, WorkerWageOffer, WorkerTask,
    WalletTransaction, WorkerSalarySettlement, AdminSupply, SupplyPurchase,
    InsurancePolicy, FarmerPolicyEnrollment, InsuranceClaim, InsuranceOfficer
)

class RegistrationValidationMixin:
    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        if phone is not None:
            phone = str(phone).strip()
        if not phone:
            raise forms.ValidationError("Phone number is required.")
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Phone number must contain exactly 10 digits.")
        return phone

    def clean_full_name(self):
        name = self.cleaned_data.get('full_name', '')
        if name is not None:
            name = name.strip()
        if not name:
            raise forms.ValidationError("Full name is required.")
        if name.isdigit():
            raise forms.ValidationError("Full name cannot contain only numbers.")
        return name

    def clean_age(self):
        if 'age' not in self.fields:
            return self.cleaned_data.get('age')
        age = self.cleaned_data.get('age')
        if age is None:
            raise forms.ValidationError("Age is required.")
        if age < 18 or age > 120:
            raise forms.ValidationError("Age must be between 18 and 120.")
        return age

    def clean_address(self):
        if 'address' not in self.fields:
            return self.cleaned_data.get('address')
        address = self.cleaned_data.get('address', '')
        if address is not None:
            address = address.strip()
        if not address:
            raise forms.ValidationError("Address is required.")
        return address

    def clean_place(self):
        if 'place' not in self.fields:
            return self.cleaned_data.get('place')
        place = self.cleaned_data.get('place', '')
        if place is not None:
            place = place.strip()
        if not place:
            raise forms.ValidationError("Place / City is required.")
        return place


# ====================================================
# LOGIN BASE & FORMS
# ====================================================

class BaseLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter registered email',
            'required': 'required'
        }),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password',
            'required': 'required'
        }),
        label='Password'
    )

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if email:
            email = email.strip()
        if not email:
            raise forms.ValidationError("Email is required.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        if not password or not password.strip():
            raise forms.ValidationError("Password is required.")
        return password


class FarmerLoginForm(BaseLoginForm):
    pass


class CustomerLoginForm(BaseLoginForm):
    pass


class WorkerLoginForm(BaseLoginForm):
    pass


class DeliveryLoginForm(BaseLoginForm):
    pass


class AdminLoginForm(BaseLoginForm):
    pass


class OfficerLoginForm(BaseLoginForm):
    pass


# ====================================================
# FARMER FORMS
# ====================================================

class FarmerRegistrationForm(RegistrationValidationMixin, forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'minlength': '6',
            'required': 'required'
        }),
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'minlength': '6',
            'required': 'required'
        }),
        label='Confirm Password'
    )

    class Meta:
        model = Farmer
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name', 'required': 'required'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age', 'min': '18', 'max': '120', 'required': 'required'}),
            'gender': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address', 'required': 'required'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Town / Village', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'pattern': '[0-9]{10}', 'maxlength': '10', 'minlength': '10', 'title': 'Phone number must contain exactly 10 digits.', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address', 'required': 'required'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if email:
            email = email.strip()
        if not email:
            raise forms.ValidationError("Email address is required.")
        if Farmer.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def clean_password(self):
        pwd = self.cleaned_data.get('password', '')
        if not pwd or not pwd.strip():
            raise forms.ValidationError("Password is required.")
        if len(pwd.strip()) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        return pwd

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class FarmerProfileForm(RegistrationValidationMixin, forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '18', 'max': '120', 'required': 'required'}),
            'gender': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': 'required'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]{10}', 'maxlength': '10', 'minlength': '10', 'title': 'Phone number must contain exactly 10 digits.', 'required': 'required'}),
        }


# ====================================================
# CUSTOMER FORMS
# ====================================================

class CustomerRegistrationForm(RegistrationValidationMixin, forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'minlength': '6',
            'required': 'required'
        }),
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'minlength': '6',
            'required': 'required'
        }),
        label='Confirm Password'
    )

    class Meta:
        model = Customer
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name', 'required': 'required'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age', 'min': '18', 'max': '120', 'required': 'required'}),
            'gender': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address', 'required': 'required'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Town / Village', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'pattern': '[0-9]{10}', 'maxlength': '10', 'minlength': '10', 'title': 'Phone number must contain exactly 10 digits.', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address', 'required': 'required'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if email:
            email = email.strip()
        if not email:
            raise forms.ValidationError("Email address is required.")
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def clean_password(self):
        pwd = self.cleaned_data.get('password', '')
        if not pwd or not pwd.strip():
            raise forms.ValidationError("Password is required.")
        if len(pwd.strip()) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        return pwd

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class CustomerProfileForm(RegistrationValidationMixin, forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '18', 'max': '120', 'required': 'required'}),
            'gender': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': 'required'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]{10}', 'maxlength': '10', 'minlength': '10', 'title': 'Phone number must contain exactly 10 digits.', 'required': 'required'}),
        }


# ====================================================
# WORKER FORMS
# ====================================================

class WorkerRegistrationForm(RegistrationValidationMixin, forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'minlength': '6',
            'required': 'required'
        }),
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'minlength': '6',
            'required': 'required'
        }),
        label='Confirm Password'
    )

    class Meta:
        model = Worker
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name', 'required': 'required'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age', 'min': '18', 'max': '120', 'required': 'required'}),
            'gender': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address', 'required': 'required'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Town / Village', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'pattern': '[0-9]{10}', 'maxlength': '10', 'minlength': '10', 'title': 'Phone number must contain exactly 10 digits.', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address', 'required': 'required'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if email:
            email = email.strip()
        if not email:
            raise forms.ValidationError("Email address is required.")
        if Worker.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def clean_password(self):
        pwd = self.cleaned_data.get('password', '')
        if not pwd or not pwd.strip():
            raise forms.ValidationError("Password is required.")
        if len(pwd.strip()) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        return pwd

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class WorkerProfileForm(RegistrationValidationMixin, forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '18', 'max': '120', 'required': 'required'}),
            'gender': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': 'required'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]{10}', 'maxlength': '10', 'minlength': '10', 'title': 'Phone number must contain exactly 10 digits.', 'required': 'required'}),
        }


# ====================================================
# DELIVERY PERSON FORMS
# ====================================================

class AdminDeliveryForm(RegistrationValidationMixin, forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter temporary password',
            'minlength': '6'
        }),
        label='Password',
        required=False
    )
    
    class Meta:
        model = Delivery
        fields = ['full_name', 'phone', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'pattern': '[0-9]{10}', 'maxlength': '10', 'minlength': '10', 'title': 'Phone number must contain exactly 10 digits.', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address', 'required': 'required'}),
        }
        
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if email:
            email = email.strip()
        if not email:
            raise forms.ValidationError("Email address is required.")
        qs = Delivery.objects.filter(email=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def clean_password(self):
        pwd = self.cleaned_data.get('password', '')
        if pwd:
            pwd = pwd.strip()
            if len(pwd) < 6:
                raise forms.ValidationError("Password must be at least 6 characters long.")
        return pwd


class DeliveryRegistrationForm(RegistrationValidationMixin, forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'minlength': '6',
            'required': 'required'
        }),
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'minlength': '6',
            'required': 'required'
        }),
        label='Confirm Password'
    )

    class Meta:
        model = Delivery
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name', 'required': 'required'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age', 'min': '18', 'max': '120', 'required': 'required'}),
            'gender': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address', 'required': 'required'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Town / Village', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'pattern': '[0-9]{10}', 'maxlength': '10', 'minlength': '10', 'title': 'Phone number must contain exactly 10 digits.', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address', 'required': 'required'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if email:
            email = email.strip()
        if not email:
            raise forms.ValidationError("Email address is required.")
        if Delivery.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def clean_password(self):
        pwd = self.cleaned_data.get('password', '')
        if not pwd or not pwd.strip():
            raise forms.ValidationError("Password is required.")
        if len(pwd.strip()) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        return pwd

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class DeliveryProfileForm(RegistrationValidationMixin, forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '18', 'max': '120', 'required': 'required'}),
            'gender': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': 'required'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]{10}', 'maxlength': '10', 'minlength': '10', 'title': 'Phone number must contain exactly 10 digits.', 'required': 'required'}),
        }


# ====================================================
# MARKETPLACE MODULE FORMS
# ====================================================

class MarketSettingsForm(forms.ModelForm):
    class Meta:
        model = MarketSettings
        fields = ['status', 'market_date', 'opening_time', 'closing_time']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select fw-bold', 'required': 'required'}),
            'market_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'required'}),
            'opening_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'required': 'required'}),
            'closing_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['market_date'].widget.attrs['min'] = timezone.now().date().isoformat()

    def clean_market_date(self):
        m_date = self.cleaned_data.get('market_date')
        if not m_date:
            raise forms.ValidationError("Market date is required.")
        if m_date < timezone.now().date():
            raise forms.ValidationError("Please select today or a future date.")
        return m_date

    def clean(self):
        cleaned_data = super().clean()
        opening = cleaned_data.get('opening_time')
        closing = cleaned_data.get('closing_time')
        if opening and closing and closing <= opening:
            self.add_error('closing_time', "Closing time must be after opening time.")
        return cleaned_data


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'description', 'quantity', 'unit', 'price_per_unit', 'image']
        widgets = {
            'product_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Organic Tomatoes',
                'required': 'required'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Vegetables, Fruits, Dairy Products',
                'required': 'required'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Detailed product description...',
                'required': 'required'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '1',
                'placeholder': 'Quantity available',
                'required': 'required'
            }),
            'unit': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'price_per_unit': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '1',
                'placeholder': 'Starting Price per Unit (₹)',
                'required': 'required'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.png, .jpg, .jpeg, image/png, image/jpeg',
                'required': 'required'
            }),
        }
        error_messages = {
            'product_name': {
                'required': "Product name is required.",
            },
            'category': {
                'required': "Category is required.",
            },
            'description': {
                'required': "Description is required.",
            },
            'quantity': {
                'required': "Quantity is required.",
                'invalid': "Enter a valid quantity.",
            },
            'unit': {
                'required': "Please select a unit.",
                'invalid_choice': "Please select a valid unit.",
            },
            'price_per_unit': {
                'required': "Starting price is required.",
                'invalid': "Enter a valid starting price.",
            },
            'image': {
                'required': "Please upload a product image.",
                'invalid': "Only valid PNG, JPG, and JPEG images are allowed.",
                'invalid_image': "Only valid PNG, JPG, and JPEG images are allowed.",
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_name'].required = True
        self.fields['category'].required = True
        self.fields['description'].required = True
        self.fields['quantity'].required = True
        self.fields['unit'].required = True
        self.fields['price_per_unit'].required = True

        # Provide a blank choice prompt for unit
        self.fields['unit'].choices = [('', 'Select Unit')] + list(Product.UNIT_CHOICES)

        # Handle image requirement:
        # When editing an existing product that already has an image, image upload is optional
        if self.instance and self.instance.pk and self.instance.image:
            self.fields['image'].required = False
            self.fields['image'].widget.attrs.pop('required', None)
        else:
            self.fields['image'].required = True
            self.fields['image'].widget.attrs['required'] = 'required'

    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name')
        if product_name is not None:
            product_name = product_name.strip()
        if not product_name:
            raise forms.ValidationError("Product name is required.")
        return product_name

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if category is not None:
            category = category.strip()
        if not category:
            raise forms.ValidationError("Category is required.")
        return category

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description is not None:
            description = description.strip()
        if not description:
            raise forms.ValidationError("Description is required.")
        return description

    def clean_unit(self):
        unit = self.cleaned_data.get('unit')
        if unit is not None:
            unit = unit.strip()
        if not unit:
            raise forms.ValidationError("Please select a unit.")
        valid_units = [c[0] for c in Product.UNIT_CHOICES]
        if unit not in valid_units:
            raise forms.ValidationError("Please select a valid unit.")
        return unit

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is None:
            raise forms.ValidationError("Quantity is required.")
        if quantity < 1:
            raise forms.ValidationError("Quantity must be at least 1.")
        return quantity

    def clean_price_per_unit(self):
        price = self.cleaned_data.get('price_per_unit')
        if price is None:
            raise forms.ValidationError("Starting price is required.")
        if price < 1:
            raise forms.ValidationError("Starting price must be at least 1.")
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            if self.instance and self.instance.pk and self.instance.image:
                return self.instance.image
            raise forms.ValidationError("Please upload a product image.")

        if hasattr(image, 'name') and image.name:
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise forms.ValidationError("Only valid PNG, JPG, and JPEG images are allowed.")

            try:
                image.seek(0)
                img = Image.open(image)
                img.verify()
                if img.format.upper() not in ['JPEG', 'PNG']:
                    raise forms.ValidationError("Only valid PNG, JPG, and JPEG images are allowed.")
                image.seek(0)
            except forms.ValidationError:
                raise
            except Exception:
                raise forms.ValidationError("Only valid PNG, JPG, and JPEG images are allowed.")
        else:
            if self.instance and self.instance.pk and self.instance.image:
                return self.instance.image
            raise forms.ValidationError("Please upload a product image.")

        return image

    def clean(self):
        cleaned_data = super().clean()
        for field in ['product_name', 'category', 'description', 'quantity', 'unit', 'price_per_unit']:
            val = cleaned_data.get(field)
            if val is None or (isinstance(val, str) and not val.strip()):
                if field not in self.errors:
                    self.add_error(field, f"{field.replace('_', ' ').capitalize()} is required.")
        image = cleaned_data.get('image')
        has_existing_image = self.instance and self.instance.pk and self.instance.image
        if not image and not has_existing_image:
            if 'image' not in self.errors:
                self.add_error('image', "Please upload a product image.")
        return cleaned_data


class BidForm(forms.ModelForm):
    class Meta:
        model = BargainingBid
        fields = ['bid_price_per_unit']
        widgets = {
            'bid_price_per_unit': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'step': '0.01', 'min': '0.01', 'placeholder': 'Enter your bid price per unit (₹)', 'required': 'required'}),
        }

    def clean_bid_price_per_unit(self):
        bid_price = self.cleaned_data.get('bid_price_per_unit')
        if bid_price is None:
            raise forms.ValidationError("Bid amount is required.")
        if bid_price <= 0:
            raise forms.ValidationError("Bid amount must be greater than 0.")
        return bid_price


# ====================================================
# WORKER MANAGEMENT & PAYMENT FORMS
# ====================================================

class AdminWorkerForm(RegistrationValidationMixin, forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter temporary password',
            'minlength': '6',
            'required': 'required'
        }),
        label='Password',
        required=True
    )
    
    class Meta:
        model = Worker
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone', 'email', 'status']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name', 'required': 'required'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age', 'min': '18', 'max': '120', 'required': 'required'}),
            'gender': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address', 'required': 'required'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Town / Village', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'pattern': '[0-9]{10}', 'maxlength': '10', 'minlength': '10', 'title': 'Phone number must contain exactly 10 digits.', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address', 'required': 'required'}),
            'status': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
        }
        
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if email:
            email = email.strip()
        if not email:
            raise forms.ValidationError("Email address is required.")
        qs = Worker.objects.filter(email=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def clean_password(self):
        pwd = self.cleaned_data.get('password', '')
        if not pwd or not pwd.strip():
            raise forms.ValidationError("Password is required.")
        if len(pwd.strip()) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        return pwd.strip()


class WorkerRequestForm(forms.ModelForm):
    class Meta:
        model = WorkerRequest
        fields = ['num_workers', 'work_description', 'location', 'start_date', 'duration_days', 'requested_wage']
        widgets = {
            'num_workers': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'Number of workers needed', 'required': 'required'}),
            'work_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe the work (e.g. Tomato Planting)', 'required': 'required'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Work location', 'required': 'required'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'required'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'Duration in days', 'required': 'required'}),
            'requested_wage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '1', 'placeholder': 'Expected Daily Wage per Worker (₹)', 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs['min'] = timezone.now().date().isoformat()

    def clean_work_description(self):
        val = self.cleaned_data.get('work_description', '')
        if val is not None:
            val = val.strip()
        if not val:
            raise forms.ValidationError("Work description is required.")
        return val

    def clean_location(self):
        val = self.cleaned_data.get('location', '')
        if val is not None:
            val = val.strip()
        if not val:
            raise forms.ValidationError("Location is required.")
        return val

    def clean_start_date(self):
        s_date = self.cleaned_data.get('start_date')
        if not s_date:
            raise forms.ValidationError("Start date is required.")
        if s_date < timezone.now().date():
            raise forms.ValidationError("Please select today or a future date.")
        return s_date

    def clean_num_workers(self):
        val = self.cleaned_data.get('num_workers')
        if val is None:
            raise forms.ValidationError("Number of workers is required.")
        if val <= 0:
            raise forms.ValidationError("Number of workers must be at least 1.")
        return val

    def clean_duration_days(self):
        val = self.cleaned_data.get('duration_days')
        if val is None:
            raise forms.ValidationError("Duration is required.")
        if val <= 0:
            raise forms.ValidationError("Duration must be at least 1 day.")
        return val

    def clean_requested_wage(self):
        val = self.cleaned_data.get('requested_wage')
        if val is None:
            raise forms.ValidationError("Expected daily wage is required.")
        if val <= 0:
            raise forms.ValidationError("Amount must be greater than 0.")
        return val


class WorkerWageOfferForm(forms.ModelForm):
    class Meta:
        model = WorkerWageOffer
        fields = ['amount_per_worker_per_day', 'message']
        widgets = {
            'amount_per_worker_per_day': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '1', 'placeholder': 'Offer amount (₹)', 'required': 'required'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional note/message'}),
        }

    def clean_amount_per_worker_per_day(self):
        val = self.cleaned_data.get('amount_per_worker_per_day')
        if val is None:
            raise forms.ValidationError("Offer amount is required.")
        if val <= 0:
            raise forms.ValidationError("Amount must be greater than 0.")
        return val

    def clean_message(self):
        msg = self.cleaned_data.get('message', '')
        if msg is not None:
            msg = msg.strip()
        return msg


class WorkerTaskForm(forms.ModelForm):
    class Meta:
        model = WorkerTask
        fields = ['work_description', 'location', 'start_date', 'duration_days']
        widgets = {
            'work_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Task Details', 'required': 'required'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Work location', 'required': 'required'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'required'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'Duration in days', 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs['min'] = timezone.now().date().isoformat()

    def clean_work_description(self):
        val = self.cleaned_data.get('work_description', '')
        if val is not None:
            val = val.strip()
        if not val:
            raise forms.ValidationError("Task details are required.")
        return val

    def clean_location(self):
        val = self.cleaned_data.get('location', '')
        if val is not None:
            val = val.strip()
        if not val:
            raise forms.ValidationError("Work location is required.")
        return val

    def clean_start_date(self):
        s_date = self.cleaned_data.get('start_date')
        if not s_date:
            raise forms.ValidationError("Start date is required.")
        if s_date < timezone.now().date():
            raise forms.ValidationError("Please select today or a future date.")
        return s_date

    def clean_duration_days(self):
        val = self.cleaned_data.get('duration_days')
        if val is None:
            raise forms.ValidationError("Duration is required.")
        if val <= 0:
            raise forms.ValidationError("Duration must be at least 1 day.")
        return val


class AdminSupplyForm(forms.ModelForm):
    class Meta:
        model = AdminSupply
        fields = ['supply_name', 'category', 'description', 'price', 'unit', 'available_quantity', 'image', 'status']
        widgets = {
            'supply_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Tomato Seeds', 'required': 'required'}),
            'category': forms.Select(choices=[
                ('', 'Select Category'),
                ('Seeds', 'Seeds'),
                ('Plants', 'Plants'),
                ('Fertilizers', 'Fertilizers'),
                ('Equipment', 'Equipment'),
                ('Other', 'Other'),
            ], attrs={'class': 'form-select', 'required': 'required'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Supply description...', 'required': 'required'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01', 'placeholder': 'Price per unit (₹)', 'required': 'required'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Packet, Kg, Bottle', 'required': 'required'}),
            'available_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': 'Available Stock', 'required': 'required'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': '.png, .jpg, .jpeg, image/png, image/jpeg'}),
            'status': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
        }
        error_messages = {
            'supply_name': {'required': "Supply name is required."},
            'category': {'required': "Category is required."},
            'description': {'required': "Description is required."},
            'price': {'required': "Price is required.", 'invalid': "Enter a valid price."},
            'unit': {'required': "Unit is required."},
            'available_quantity': {'required': "Available quantity is required.", 'invalid': "Enter a valid quantity."},
            'image': {'invalid_image': "Only valid PNG, JPG, and JPEG images are allowed."}
        }

    def clean_supply_name(self):
        name = self.cleaned_data.get('supply_name', '')
        if name:
            name = name.strip()
        if not name:
            raise forms.ValidationError("Supply name is required.")
        return name

    def clean_category(self):
        cat = self.cleaned_data.get('category', '')
        if cat:
            cat = cat.strip()
        if not cat:
            raise forms.ValidationError("Category is required.")
        return cat

    def clean_description(self):
        desc = self.cleaned_data.get('description', '')
        if desc:
            desc = desc.strip()
        if not desc:
            raise forms.ValidationError("Description is required.")
        return desc

    def clean_unit(self):
        unit = self.cleaned_data.get('unit', '')
        if unit:
            unit = unit.strip()
        if not unit:
            raise forms.ValidationError("Unit is required.")
        return unit

    def clean_price(self):
        val = self.cleaned_data.get('price')
        if val is None:
            raise forms.ValidationError("Price is required.")
        if val <= 0:
            raise forms.ValidationError("Price must be greater than 0.")
        return val

    def clean_available_quantity(self):
        qty = self.cleaned_data.get('available_quantity')
        if qty is None:
            raise forms.ValidationError("Available quantity is required.")
        if qty < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return qty

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            if self.instance and self.instance.pk and self.instance.image:
                return self.instance.image
            return image

        if hasattr(image, 'name') and image.name:
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise forms.ValidationError("Only valid PNG, JPG, and JPEG images are allowed.")
            
            try:
                image.seek(0)
                img = Image.open(image)
                img.verify()
                if img.format.upper() not in ['JPEG', 'PNG']:
                    raise forms.ValidationError("Only valid PNG, JPG, and JPEG images are allowed.")
                image.seek(0)
            except forms.ValidationError:
                raise
            except Exception:
                raise forms.ValidationError("Only valid PNG, JPG, and JPEG images are allowed.")
                
        return image


# ====================================================
# AGRICULTURAL INSURANCE FORMS
# ====================================================

class InsurancePolicyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today_iso = timezone.now().date().isoformat()
        self.fields['coverage_start_date'].widget.attrs['min'] = today_iso
        self.fields['coverage_end_date'].widget.attrs['min'] = today_iso
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
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Tomato Crop Protection Policy', 'required': 'required'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': 'required'}),
            'eligible_crop': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Tomato', 'required': 'required'}),
            'covered_risks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'e.g. Flood, Heavy Rainfall, Inundation', 'required': 'required'}),
            'max_coverage_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01', 'placeholder': 'e.g. 50000.00', 'required': 'required'}),
            'premium_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01', 'placeholder': '2000.00', 'required': 'required'}),
            'coverage_duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1 Year', 'required': 'required'}),
            'payment_frequency': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'coverage_start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'required'}),
            'coverage_end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'required'}),
            'claim_reporting_deadline_days': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'required': 'required'}),
            'terms_and_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': 'required'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_name(self):
        v = self.cleaned_data.get('name', '')
        if v:
            v = v.strip()
        if not v:
            raise forms.ValidationError("Policy name is required.")
        return v

    def clean_description(self):
        v = self.cleaned_data.get('description', '')
        if v:
            v = v.strip()
        if not v:
            raise forms.ValidationError("Description is required.")
        return v

    def clean_eligible_crop(self):
        v = self.cleaned_data.get('eligible_crop', '')
        if v:
            v = v.strip()
        if not v:
            raise forms.ValidationError("Eligible crop is required.")
        return v

    def clean_covered_risks(self):
        v = self.cleaned_data.get('covered_risks', '')
        if v:
            v = v.strip()
        if not v:
            raise forms.ValidationError("Covered risks are required.")
        return v

    def clean_coverage_duration(self):
        v = self.cleaned_data.get('coverage_duration', '')
        if v:
            v = v.strip()
        if not v:
            raise forms.ValidationError("Coverage duration is required.")
        return v

    def clean_terms_and_conditions(self):
        v = self.cleaned_data.get('terms_and_conditions', '')
        if v:
            v = v.strip()
        if not v:
            raise forms.ValidationError("Terms and conditions are required.")
        return v

    def clean_coverage_start_date(self):
        start = self.cleaned_data.get('coverage_start_date')
        if not start:
            raise forms.ValidationError("Coverage start date is required.")
        if not self.instance.pk and start < timezone.now().date():
            raise forms.ValidationError("Please select today or a future date.")
        return start

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('coverage_start_date')
        end = cleaned_data.get('coverage_end_date')
        max_cov = cleaned_data.get('max_coverage_amount')
        prem = cleaned_data.get('premium_amount')
        deadline = cleaned_data.get('claim_reporting_deadline_days')

        if start and end and end <= start:
            self.add_error('coverage_end_date', "Coverage end date must be after coverage start date.")
        if max_cov is not None and max_cov <= 0:
            self.add_error('max_coverage_amount', "Maximum coverage amount must be greater than zero.")
        if prem is not None and prem <= 0:
            self.add_error('premium_amount', "Annual premium amount must be greater than zero.")
        if deadline is not None and deadline < 1:
            self.add_error('claim_reporting_deadline_days', "Claim reporting deadline must be at least 1 day.")
        return cleaned_data


class FarmerPolicyEnrollmentForm(forms.ModelForm):
    class Meta:
        model = FarmerPolicyEnrollment
        fields = ['crop_name', 'farm_area', 'farm_location']
        widgets = {
            'crop_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter crop name', 'required': 'required'}),
            'farm_area': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01', 'placeholder': 'Farm area in acres', 'required': 'required'}),
            'farm_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Farm location/address', 'required': 'required'}),
        }

    def clean_crop_name(self):
        v = self.cleaned_data.get('crop_name', '')
        if v:
            v = v.strip()
        if not v:
            raise forms.ValidationError("Crop name is required.")
        return v

    def clean_farm_location(self):
        v = self.cleaned_data.get('farm_location', '')
        if v:
            v = v.strip()
        if not v:
            raise forms.ValidationError("Farm location is required.")
        return v

    def clean_farm_area(self):
        farm_area = self.cleaned_data.get('farm_area')
        if farm_area is None:
            raise forms.ValidationError("Farm area is required.")
        if farm_area <= 0:
            raise forms.ValidationError("Farm area must be greater than zero.")
        return farm_area


class InsuranceClaimForm(forms.ModelForm):
    class Meta:
        model = InsuranceClaim
        fields = ['incident_type', 'incident_date', 'incident_location', 'damage_description', 
                  'affected_farm_area', 'estimated_financial_loss', 'evidence_file']
        widgets = {
            'incident_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Flood / Heavy Rainfall', 'required': 'required'}),
            'incident_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'required'}),
            'incident_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Incident location', 'required': 'required'}),
            'damage_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detailed description of crop damage', 'required': 'required'}),
            'affected_farm_area': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01', 'placeholder': 'Acres affected', 'required': 'required'}),
            'estimated_financial_loss': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01', 'placeholder': '₹ Estimated loss', 'required': 'required'}),
            'evidence_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.png, .jpg, .jpeg, .pdf, image/png, image/jpeg, application/pdf'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['incident_date'].widget.attrs['max'] = timezone.now().date().isoformat()

    def clean_incident_type(self):
        v = self.cleaned_data.get('incident_type', '')
        if v:
            v = v.strip()
        if not v:
            raise forms.ValidationError("Incident type is required.")
        return v

    def clean_incident_location(self):
        v = self.cleaned_data.get('incident_location', '')
        if v:
            v = v.strip()
        if not v:
            raise forms.ValidationError("Incident location is required.")
        return v

    def clean_damage_description(self):
        v = self.cleaned_data.get('damage_description', '')
        if v:
            v = v.strip()
        if not v:
            raise forms.ValidationError("Damage description is required.")
        return v

    def clean_incident_date(self):
        incident_date = self.cleaned_data.get('incident_date')
        if not incident_date:
            raise forms.ValidationError("Incident date is required.")
        if incident_date > timezone.now().date():
            raise forms.ValidationError("Incident date cannot be in the future.")
        return incident_date

    def clean_estimated_financial_loss(self):
        loss = self.cleaned_data.get('estimated_financial_loss')
        if loss is None:
            raise forms.ValidationError("Estimated financial loss is required.")
        if loss <= 0:
            raise forms.ValidationError("Estimated financial loss must be greater than zero.")
        return loss

    def clean_affected_farm_area(self):
        area = self.cleaned_data.get('affected_farm_area')
        if area is None:
            raise forms.ValidationError("Affected farm area is required.")
        if area <= 0:
            raise forms.ValidationError("Affected farm area must be greater than zero.")
        return area

    def clean_evidence_file(self):
        file = self.cleaned_data.get('evidence_file')
        if not file:
            return file
        if hasattr(file, 'name') and file.name:
            ext = os.path.splitext(file.name)[1].lower()
            allowed = ['.png', '.jpg', '.jpeg', '.pdf']
            if ext not in allowed:
                raise forms.ValidationError("Only valid PNG, JPG, JPEG images or PDF documents are allowed.")
            if ext in ['.png', '.jpg', '.jpeg']:
                try:
                    file.seek(0)
                    img = Image.open(file)
                    img.verify()
                    if img.format.upper() not in ['JPEG', 'PNG']:
                        raise forms.ValidationError("Only valid PNG, JPG, and JPEG images are allowed.")
                    file.seek(0)
                except forms.ValidationError:
                    raise
                except Exception:
                    raise forms.ValidationError("Only valid PNG, JPG, and JPEG images are allowed.")
        return file


class ClaimReviewForm(forms.ModelForm):
    class Meta:
        model = InsuranceClaim
        fields = ['status', 'officer_notes', 'rejection_reason', 'approved_amount']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'officer_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rejection_reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'approved_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        approved_amount = cleaned_data.get('approved_amount')
        rejection_reason = cleaned_data.get('rejection_reason', '')

        if status == 'APPROVED':
            if approved_amount is None or approved_amount <= 0:
                self.add_error('approved_amount', "Approved amount must be greater than zero when approving a claim.")
        elif status == 'REJECTED':
            if not rejection_reason or not rejection_reason.strip():
                self.add_error('rejection_reason', "Rejection reason is required when rejecting a claim.")
        return cleaned_data


class InsuranceOfficerForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter temporary password', 'minlength': '6', 'required': 'required'}),
        label='Password'
    )
    class Meta:
        model = InsuranceOfficer
        fields = ['full_name', 'email', 'phone', 'is_active']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Officer Name', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'pattern': '[0-9]{10}', 'maxlength': '10', 'minlength': '10', 'title': 'Phone number must contain exactly 10 digits.', 'required': 'required'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def clean_full_name(self):
        name = self.cleaned_data.get('full_name', '')
        if name:
            name = name.strip()
        if not name:
            raise forms.ValidationError("Officer name is required.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        if phone:
            phone = str(phone).strip()
        if not phone:
            raise forms.ValidationError("Phone number is required.")
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Phone number must contain exactly 10 digits.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if email:
            email = email.strip()
        if not email:
            raise forms.ValidationError("Email address is required.")
        qs = InsuranceOfficer.objects.filter(email=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("An officer with this email address already exists.")
        return email

    def clean_password(self):
        pwd = self.cleaned_data.get('password', '')
        if not pwd or not pwd.strip():
            raise forms.ValidationError("Password is required.")
        if len(pwd.strip()) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        return pwd.strip()
