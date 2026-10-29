import os
import glob
import sys
import django

# Clean old db and migration files
db_file = r'C:\Users\TGM\.gemini\antigravity\scratch\buxdu_smart_admin\demo_app\db.sqlite3'
if os.path.exists(db_file):
    os.remove(db_file)
    print("Removed old db.sqlite3")

mig_files = glob.glob(r'C:\Users\TGM\.gemini\antigravity\scratch\buxdu_smart_admin\demo_app\news\migrations\[0-9]*.py')
for f in mig_files:
    os.remove(f)
    print(f"Removed migration: {f}")

sys.path.insert(0, r'C:\Users\TGM\.gemini\antigravity\scratch\buxdu_smart_admin\demo_app')
sys.path.insert(0, r'C:\Users\TGM\.gemini\antigravity\scratch\buxdu_smart_admin')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_core.settings')

django.setup()

from django.core.management import call_command

print("Creating initial migrations...")
call_command('makemigrations', 'news')

print("Applying migrations...")
call_command('migrate')

# Create superuser
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@buxdu.uz', 'admin123')
    print("Created superuser: admin / admin123")

print("Migration completed!")
