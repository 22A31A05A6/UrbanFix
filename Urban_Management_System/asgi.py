import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Urban_Management_System.settings')
application = get_asgi_application()
