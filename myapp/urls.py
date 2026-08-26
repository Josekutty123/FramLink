from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('choose-login/', views.choose_login_view, name='choose_login'),
    
    # Farmer Module URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('farmer/login/', views.login_view, name='farmer_login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),

    # Customer Module URLs
    path('customer/register/', views.customer_register_view, name='customer_register'),
    path('customer/login/', views.customer_login_view, name='customer_login'),
    path('customer/dashboard/', views.customer_dashboard_view, name='customer_dashboard'),
    path('customer/live-rooms/', views.customer_live_rooms_view, name='customer_live_rooms'),
    path('customer/my-bids/', views.customer_bids_view, name='customer_bids'),
    path('customer/profile/', views.customer_profile_view, name='customer_profile'),
    path('customer/logout/', views.customer_logout_view, name='customer_logout'),

    # Worker Module URLs
    path('worker/register/', views.worker_register_view, name='worker_register'),
    path('worker/login/', views.worker_login_view, name='worker_login'),
    path('worker/dashboard/', views.worker_dashboard_view, name='worker_dashboard'),
    path('worker/profile/', views.worker_profile_view, name='worker_profile'),
    path('worker/logout/', views.worker_logout_view, name='worker_logout'),

    # Delivery Person Module URLs
    path('delivery/login/', views.delivery_login_view, name='delivery_login'),
    path('delivery/dashboard/', views.delivery_dashboard_view, name='delivery_dashboard'),
    path('delivery/profile/', views.delivery_profile_view, name='delivery_profile'),
    path('delivery/logout/', views.delivery_logout_view, name='delivery_logout'),
    path('delivery/update-status/<str:order_id>/', views.delivery_update_status_view, name='delivery_update_status'),

    # Admin Module URLs
    path('admin/login/', views.admin_login_view, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin/farmers/', views.admin_farmers_view, name='admin_farmers'),
    path('admin/farmers/<int:pk>/', views.admin_farmer_detail_view, name='admin_farmer_detail'),
    path('admin/customers/', views.admin_customers_view, name='admin_customers'),
    path('admin/customers/<str:customer_id>/', views.admin_customer_detail_view, name='admin_customer_detail'),
    path('admin/deliveries/', views.admin_deliveries_view, name='admin_deliveries'),
    path('admin/deliveries/add/', views.admin_add_delivery_view, name='admin_add_delivery'),
    path('admin/deliveries/<str:delivery_id>/', views.admin_delivery_detail_view, name='admin_delivery_detail'),
    path('admin/deliveries/edit/<str:delivery_id>/', views.admin_edit_delivery_view, name='admin_edit_delivery'),
    path('admin/deliveries/toggle/<str:delivery_id>/', views.admin_toggle_delivery_view, name='admin_toggle_delivery'),
    path('admin/deliveries/assign/<str:order_id>/', views.admin_assign_delivery_view, name='admin_assign_delivery'),
    path('admin/deliveries/assign-action/<str:order_id>/', views.admin_assign_delivery_action_view, name='admin_assign_delivery_action'),
    path('admin/live-rooms/', views.admin_live_rooms_view, name='admin_live_rooms'),
    path('admin/logout/', views.admin_logout_view, name='admin_logout'),

    # Marketplace Module URLs
    path('admin/marketplace/', views.admin_marketplace_view, name='admin_marketplace'),
    path('admin/marketplace/action/<str:action>/', views.admin_market_action_view, name='admin_market_action'),
    path('admin/wallet/', views.admin_wallet_view, name='admin_wallet'),
    path('admin/sales/', views.admin_sales_history_view, name='admin_sales_history'),
    path('admin/sales/<str:sale_id>/', views.admin_sale_details_view, name='admin_sale_details'),

    path('farmer/products/', views.farmer_products_view, name='farmer_products'),
    path('farmer/products/add/', views.farmer_add_product_view, name='farmer_add_product'),
    path('farmer/products/edit/<str:product_id>/', views.farmer_edit_product_view, name='farmer_edit_product'),
    path('farmer/products/delete/<str:product_id>/', views.farmer_delete_product_view, name='farmer_delete_product'),
    path('farmer/wallet/', views.farmer_wallet_view, name='farmer_wallet'),

    path('explore-products/', views.explore_products_view, name='explore_products'),
    path('marketplace/join/<str:product_id>/', views.join_bargaining_view, name='join_bargaining'),
    path('live-bargaining/<str:product_id>/', views.live_bargaining_view, name='live_bargaining'),
    
    # API endpoints for Live Bargaining
    path('api/place-bid/<str:product_id>/', views.api_place_bid_view, name='api_place_bid'),
    path('api/bids/<str:product_id>/', views.api_get_bids_view, name='api_get_bids'),
]
