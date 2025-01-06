from pathlib import Path
import os
import logging

logging.basicConfig(level=logging.DEBUG)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "SECRET_KEY"

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'main',
    'accounts',
    'goods',
    'cart',
    'reviews',
    'orders',
    'analytics',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "orders.middleware.TimeBasedAccessMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "FlowerDelivery.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS":  [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "FlowerDelivery.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

#-------------------------------------------------------------------------
# Секция, в которой заданы параметры SMTP,
# чтобы Django мог отправлять электронные письма
# для восстановления пароля пользователя

# Теперь через google
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST =  'smtp.your-email-provider.com'  # Нужно заполнить

EMAIL_PORT = 587 # Для TLS
EMAIL_USE_TLS = True # Для TLS

# EMAIL_PORT = 465  # Для SSL
# EMAIL_USE_SSL = True # Для TLS

EMAIL_HOST_USER = 'your-email@example.com'    # Нужно заполнить
EMAIL_HOST_PASSWORD = 'your-email-password'   # Нужно заполнить

# Конец секции с параметрами SMTP

#-------------------------------------------------------------------------
# Секция, в которой заданы глобальные переменные этого проекта

COMMON_DICT = {
       'caption': 'FlowerDelivery',
       'country': 'Российская Федерация',
       'town': 'Ростов-на-Дону',
       'year': '2025',

       # Время работы магазина:
       'start_time': '8:00',  # Начало рабочего дня
       'end_time': '22:00',   # Конец рабочего дня

        # Временные интервалы для доставки:
       'delivery_time_intervals' : ['09:00 - 11:00', '11:00 - 13:00', '13:00 - 15:00', '15:00 - 17:00', '17:00 - 19:00','19:00 - 21:00']
   }

TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
TELEGRAM_CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID'

# Конец секции с глобальными переменными этого проекта
#-------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru"

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
