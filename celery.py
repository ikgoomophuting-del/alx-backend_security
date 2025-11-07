import os
from celery import celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx-backend_security.settings')

app = celery('alx-backend_security')

# Load configuration from Django settings, using a namespace to prevent collisions.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks from all registered Django app configs.
app.autodiscover_tasks()

# Optional: define scheduled (periodic) tasks
app.conf.beat_schedule = {
    'detect-suspicious-ips-hourly': {
        'task': 'ip_tracking.tasks.detect_suspicious_activity',
        'schedule': crontab(minute=0, hour='*'),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
