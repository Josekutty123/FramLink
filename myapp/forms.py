from django import forms
from .models import Farmer, Customer, Worker, Delivery, MarketSettings, Product, BargainingBid, WorkerRequest, WorkerWageOffer, WorkerTask, WalletTransaction, WorkerSalarySettlement


class FarmerRegistrationForm(forms.ModelForm):
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
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
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


class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '18', 'max': '120'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
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

class CustomerRegistrationForm(forms.ModelForm):
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
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
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


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '18', 'max': '120'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


# ====================================================
# WORKER FORMS
# ====================================================

class WorkerRegistrationForm(forms.ModelForm):
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
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
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


class WorkerProfileForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '18', 'max': '120'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


# ====================================================
# DELIVERY PERSON FORMS
# ====================================================

class AdminDeliveryForm(forms.ModelForm):
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
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
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


class DeliveryRegistrationForm(forms.ModelForm):
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
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
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


class DeliveryProfileForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['full_name', 'age', 'gender', 'address', 'place', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '18', 'max': '120'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
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
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01', 'placeholder': 'Quantity available'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'price_per_unit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01', 'placeholder': 'Starting Price per Unit (₹)'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }



class BidForm(forms.ModelForm):
    class Meta:
        model = BargainingBid
        fields = ['bid_price_per_unit']
        widgets = {
            'bid_price_per_unit': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'step': '0.01', 'min': '0.01', 'placeholder': 'Enter your bid price per unit (₹)'}),
        }

# ====================================================
# WORKER MANAGEMENT & PAYMENT FORMS
# ====================================================

class AdminWorkerForm(forms.ModelForm):
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


class WorkerWageOfferForm(forms.ModelForm):
    class Meta:
        model = WorkerWageOffer
        fields = ['amount_per_worker_per_day', 'message']
        widgets = {
            'amount_per_worker_per_day': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '1', 'placeholder': 'Offer amount (₹)'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional note/message'}),
        }


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
