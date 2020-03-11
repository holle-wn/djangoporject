import os
import django
from django.core.cache import cache
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helloword.settings')
django.setup()

cache.set('ll', 'list')
print(cache.get('ll'))
