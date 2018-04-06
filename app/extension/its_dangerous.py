from flask import current_app
from itsdangerous import URLSafeTimedSerializer

url_safe_timed_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
