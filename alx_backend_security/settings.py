from celery.schedules import crontab


CELERY_BROKER_URL = 'amqp://guest:guest@localhost//'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULE = {
    'detect-suspicious-ips-hourly': {
        'task': 'ip_tracking.tasks.detect_suspicious_activity',
        'schedule': crontab(minute=0, hour='*'),
    },
}


INSTALLED_APPS = [
    # default Django apps...
    'ratelimit',
    'ip_tracking',
    'ip_tracking.apps.IpTrackingConfig',
    'django_celery_results',
]

MIDDLEWARE = [
    # Default Django middlewares...
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Custom IP tracking middleware
    'ip_tracking.middleware.RequestLoggingMiddleware',
]

ALLOWED_HOSTS = ['yourapp.pythonanywhere.com', 'yourapp.onrender.com', 'localhost']
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = '/static/'

