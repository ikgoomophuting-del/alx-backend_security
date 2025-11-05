from celery.schedules import crontab

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
