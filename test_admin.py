import os
import sys
import django

sys.path.append(r'c:\Users\Asus\python-project\MCA_Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'framelink.settings')
django.setup()

from django.test import RequestFactory
from myapp.models import Admin
from myapp.views import admin_add_delivery_view
import traceback
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware

admin = Admin.objects.first()

factory = RequestFactory()
request = factory.get('/admin/deliveries/add/')
middleware = SessionMiddleware(lambda req: None)
middleware.process_request(request)
request.session.save()
msg_middleware = MessageMiddleware(lambda req: None)
msg_middleware.process_request(request)

request.session['admin_id'] = admin.id
request.session['admin_email'] = admin.email
request.session['admin_name'] = admin.name
request.session.save()

try:
    response = admin_add_delivery_view(request)
    if hasattr(response, 'render'):
        response.render()
    print('STATUS CODE:', response.status_code)
except Exception as e:
    print('EXCEPTION OCCURRED:')
    traceback.print_exc()

