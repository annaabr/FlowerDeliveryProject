from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-84pz(fg*oxui97qm(s0(8b2^5)*$w$8t20mv%+)dv@h&$tq$e#"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

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
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
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


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

#------------------------------------------------------------------------
# Восстановление пароля через почту

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.com'                     # 'smtp.example.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER =  'annaabr@yandex.ru'             # 'your_email@example.com'
EMAIL_HOST_PASSWORD =  'AnnaYandex1969'            # 'your_email_password'
DEFAULT_FROM_EMAIL = 'annaabr@yandex.ru'           # 'your_email@example.com'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.yandex.com'  # SMTP-сервер Яндекс.Почты
# EMAIL_PORT = 587  # Порт для TLS (или 465 для SSL)
# EMAIL_USE_TLS = True  # Использовать TLS
# EMAIL_HOST_USER = 'your_email@yandex.ru'  # Ваш адрес электронной почты Яндекс
# EMAIL_HOST_PASSWORD = 'your_password'  # Ваш пароль от Яндекс.Почты

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

TELEGRAM_BOT_TOKEN = '7103387978:AAHPys-AhKpYN2YD3YC8ua-i_xFNZpDDkk0'
TELEGRAM_CHAT_ID = '708732931'

# Конец секции с глобальными переменными этого проекта
#-------------------------------------------------------------------------

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
