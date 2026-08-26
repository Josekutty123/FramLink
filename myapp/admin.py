from django.contrib import admin
from .models import Farmer

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('farmer_id', 'full_name', 'email', 'phone', 'place', 'joining_date')
    search_fields = ('farmer_id', 'full_name', 'email', 'phone', 'place')
    readonly_fields = ('farmer_id', 'joining_date', 'password')
    list_filter = ('gender', 'joining_date')
