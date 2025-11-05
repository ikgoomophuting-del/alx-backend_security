from ip_tracking.models import RequestLog
RequestLog.objects.all()
python manage.py makemigrations ip_tracking
python manage.py migrate
python manage.py runserver
python manage.py shell
