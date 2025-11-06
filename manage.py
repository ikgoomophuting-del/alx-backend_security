from ip_tracking.models import RequestLog
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_security.settings')
RequestLog.objects.all()
python manage.py makemigrations ip_tracking
python manage.py migrate
python manage.py runserver
python manage.py shell
