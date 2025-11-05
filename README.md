# ALX Backend Security - IP Tracking Milestone

This Django app provides middleware and utilities for:
- Logging request IPs, timestamps, and paths
- Blocking blacklisted IPs
- Geolocating requests (country & city)
- Applying rate limits
- Detecting anomalies via Celery

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/alx-backend-security.git
   cd alx-backend-security

2. Install dependencies:
   
pip install -r requirements.txt

3. Run migrations:

   python manage.py migrate

4. Start server:

   python manage.py runserver
---

 Useful Commands
python manage.py block_ip 192.168.1.10
celery -A alx_backend_security worker -B

---
Folder Structure

alx-backend-security/
│
├── ip_tracking/
│   ├── __init__.py
│   ├── models.py
│   ├── middleware.py
│   ├── views.py
│   ├── tasks.py
│   └── management/
│       └── commands/
│           └── block_ip.py
│
└── settings.py

---

##  `requirements.txt`
```text
Django>=4.2
django-ratelimit>=3.0
django-ipgeolocation>=1.4
celery>=5.3
redis>=5.0
requests


