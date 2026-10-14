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
    path('customer/confirm-delivery/<str:order_id>/', views.customer_confirm_delivery_view, name='customer_confirm_delivery'),

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

    path('admin/insurance/officers/', views.admin_officers_view, name='admin_officers'),
    path('admin/insurance/officers/add/', views.admin_add_officer_view, name='admin_add_officer'),
    path('admin/insurance/officers/toggle/<str:officer_id>/', views.admin_toggle_officer_view, name='admin_toggle_officer'),
    path('admin/insurance/dashboard/', views.admin_insurance_dashboard_view, name='admin_insurance_dashboard'),
    
    # Marketplace Module URLs
    path('admin/marketplace/', views.admin_marketplace_view, name='admin_marketplace'),
    path('admin/marketplace/action/<str:action>/', views.admin_market_action_view, name='admin_market_action'),
    path('admin/wallet/', views.admin_wallet_view, name='admin_wallet'),
    path('admin/sales/', views.admin_sales_history_view, name='admin_sales_history'),
    path('admin/sales/<str:sale_id>/', views.admin_sale_details_view, name='admin_sale_details'),
    
    # Admin Farm Supplies URLs
    path('admin/supplies/', views.admin_supplies_view, name='admin_supplies'),
    path('admin/supplies/add/', views.admin_add_supply_view, name='admin_add_supply'),
    path('admin/supplies/edit/<str:supply_id>/', views.admin_edit_supply_view, name='admin_edit_supply'),
    path('admin/supplies/delete/<str:supply_id>/', views.admin_delete_supply_view, name='admin_delete_supply'),
    path('admin/supplies/sales/', views.admin_supply_sales_view, name='admin_supply_sales'),

    path('farmer/products/', views.farmer_products_view, name='farmer_products'),
    path('farmer/products/add/', views.farmer_add_product_view, name='farmer_add_product'),
    path('farmer/products/edit/<str:product_id>/', views.farmer_edit_product_view, name='farmer_edit_product'),
    path('farmer/products/delete/<str:product_id>/', views.farmer_delete_product_view, name='farmer_delete_product'),
    path('farmer/wallet/', views.farmer_wallet_view, name='farmer_wallet'),
    path('farmer/wallet/topup/', views.farmer_wallet_topup_view, name='farmer_wallet_topup'),
    path('farmer/my-bids/', views.farmer_bids_view, name='farmer_bids'),
    path('farmer/confirm-delivery/<str:order_id>/', views.farmer_confirm_delivery_view, name='farmer_confirm_delivery'),
    
    # Farmer Farm Supplies URLs
    path('farmer/supplies/', views.farmer_buy_supplies_view, name='farmer_buy_supplies'),
    path('farmer/supplies/purchase/<str:supply_id>/', views.farmer_purchase_supply_view, name='farmer_purchase_supply'),
    path('farmer/supplies/purchases/', views.farmer_supply_purchases_view, name='farmer_supply_purchases'),

    path('explore-products/', views.explore_products_view, name='explore_products'),
    path('marketplace/join/<str:product_id>/', views.join_bargaining_view, name='join_bargaining'),
    path('live-bargaining/<str:product_id>/', views.live_bargaining_view, name='live_bargaining'),
    
    # API endpoints for Live Bargaining
    path('api/place-bid/<str:product_id>/', views.api_place_bid_view, name='api_place_bid'),
    path('api/bids/<str:product_id>/', views.api_get_bids_view, name='api_get_bids'),
    
    # Worker Flow Admin URLs
    path('admin/workers/', views.admin_workers_view, name='admin_workers'),
    path('admin/workers/add/', views.admin_add_worker_view, name='admin_add_worker'),
    path('admin/workers/requests/', views.admin_worker_requests_view, name='admin_worker_requests'),
    path('admin/workers/requests/<str:request_id>/negotiate/', views.admin_wage_negotiation_view, name='admin_wage_negotiation'),
    path('admin/workers/requests/<str:request_id>/assign/', views.admin_assign_workers_view, name='admin_assign_workers'),
    path('admin/workers/settlements/', views.admin_salary_settlements_view, name='admin_salary_settlements'),
    path('admin/workers/settlements/<str:settlement_id>/pay/', views.admin_pay_worker_view, name='admin_pay_worker'),

    # Worker Flow Farmer URLs
    path('farmer/workers/requests/', views.farmer_worker_requests_view, name='farmer_worker_requests'),
    path('farmer/workers/request/', views.farmer_request_workers_view, name='farmer_request_workers'),
    path('farmer/workers/requests/<str:request_id>/negotiate/', views.farmer_wage_negotiation_view, name='farmer_wage_negotiation'),
    path('farmer/workers/requests/<str:request_id>/task/create/', views.farmer_create_task_view, name='farmer_create_task'),
    path('farmer/workers/tasks/', views.farmer_tasks_view, name='farmer_tasks'),
    path('farmer/workers/tasks/<str:task_id>/confirm/', views.farmer_confirm_task_view, name='farmer_confirm_task'),
    path('farmer/workers/tasks/<str:task_id>/payment/', views.farmer_worker_payment_view, name='farmer_worker_payment'),
    
    # Worker Task update url
    path('worker/task/<str:task_id>/complete/', views.worker_mark_task_completed_view, name='worker_mark_task_completed'),
    
    # API endpoint for AI Chatbot
    path('api/ai/chat/', views.ai_chat_view, name='ai_chat'),
    
    # Insurance Officer URLs
    path('officer/login/', views.officer_login_view, name='officer_login'),
    path('officer/dashboard/', views.officer_dashboard_view, name='officer_dashboard'),
    path('officer/logout/', views.officer_logout_view, name='officer_logout'),
    path('officer/policies/', views.officer_policies_view, name='officer_policies'),
    path('officer/policies/add/', views.officer_add_policy_view, name='officer_add_policy'),
    path('officer/policies/edit/<str:policy_id>/', views.officer_edit_policy_view, name='officer_edit_policy'),
    path('officer/policies/toggle/<str:policy_id>/', views.officer_toggle_policy_view, name='officer_toggle_policy'),
    path('officer/enrollments/', views.officer_enrollments_view, name='officer_enrollments'),
    path('officer/premiums/', views.officer_premiums_view, name='officer_premiums'),
    path('officer/claims/', views.officer_claims_view, name='officer_claims'),
    path('officer/claims/<str:claim_id>/', views.officer_claim_detail_view, name='officer_claim_detail'),
    path('officer/settlements/', views.officer_settlements_view, name='officer_settlements'),
    path('officer/settlements/<str:claim_id>/settle/', views.officer_settle_claim_view, name='officer_settle_claim'),
    
    # Farmer Insurance URLs
    path('farmer/insurance/', views.farmer_insurance_view, name='farmer_insurance'),
    path('farmer/insurance/buy/<str:policy_id>/', views.farmer_buy_insurance_view, name='farmer_buy_insurance'),
    path('farmer/insurance/my-policies/', views.farmer_my_policies_view, name='farmer_my_policies'),
    path('farmer/insurance/premium/pay/<str:enrollment_id>/', views.farmer_pay_premium_view, name='farmer_pay_premium'),
    path('farmer/insurance/renew/<str:enrollment_id>/', views.farmer_renew_policy_view, name='farmer_renew_policy'),
    path('farmer/insurance/receipt/<str:payment_id>/', views.farmer_payment_receipt_view, name='farmer_payment_receipt'),
    path('farmer/insurance/premium-history/', views.farmer_premium_history_view, name='farmer_premium_history'),
    path('farmer/insurance/claim/apply/', views.farmer_apply_claim_view, name='farmer_apply_claim'),
    path('farmer/insurance/my-claims/', views.farmer_my_claims_view, name='farmer_my_claims'),
]
