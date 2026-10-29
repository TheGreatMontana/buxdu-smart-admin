import os
import sys
from pathlib import Path
import django

# Setup cross-platform paths
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_core.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model

print("1. Migrations...")
call_command('makemigrations', 'news')
call_command('migrate')

print("2. Superuser check (admin / admin123)...")
User = get_user_model()
admin_user = User.objects.filter(username='admin').first()
if not admin_user:
    User.objects.create_superuser('admin', 'admin@buxdu.uz', 'admin123')
    print("   Created superuser: admin / admin123")
else:
    admin_user.set_password('admin123')
    admin_user.save()
    print("   Superuser 'admin' ready.")

print("✅ Database is ready and completely empty of test data.")
