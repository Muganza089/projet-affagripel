from pathlib import Path
import os

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# ⚠ override=True : le .env est la SOURCE DE VÉRITÉ.
# Il écrase toute variable déjà posée dans le shell ($env: / export).
load_dotenv(BASE_DIR / ".env", override=True)


def env_bool(name, default="False"):
    return os.environ.get(name, default).strip().lower() in ("true", "1", "yes")


def env_list(name, default=""):
    return [v.strip() for v in os.environ.get(name, default).split(",") if v.strip()]


# ═══════════════════════════════════════════════════════════════
# SÉCURITÉ
# ═══════════════════════════════════════════════════════════════
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "c%+_15#vjbllro0m%ywym!eapupmdy8^l3t@iv3jyjcea=$x*o",  # fallback dev
)
DEBUG = env_bool("DJANGO_DEBUG", "False")
ALLOWED_HOSTS = [
    "affagripel-lualaba.com",
    "www.affagripel-lualaba.com",
    "server1.affagripel-lualaba.com",
    "162.254.37.75",
    "127.0.0.1",
    "localhost",
]

SESSION_ENGINE = "django.contrib.sessions.backends.db"

# ═══════════════════════════════════════════════════════════════
# APPLICATIONS
# ═══════════════════════════════════════════════════════════════
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "tailwind",
    "corsheaders",
    "rest_framework",
    "altis",
]

# ⚠ CorsMiddleware DOIT être en position 1, avant SecurityMiddleware.
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "affagripelderu.urls"
WSGI_APPLICATION = "affagripelderu.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ═══════════════════════════════════════════════════════════════
# BASE DE DONNÉES
# ═══════════════════════════════════════════════════════════════
if os.environ.get("ENVIRONMENT") == "production":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DB_NAME", "affagripel"),
            "USER": os.environ.get("DB_USER", "django_user"),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "HOST": os.environ.get("DB_HOST", "localhost"),
            "PORT": os.environ.get("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "fr"
TIME_ZONE = "Africa/Lubumbashi"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ═══════════════════════════════════════════════════════════════
# ALTIS SPHERE — CORS scopé sur /api/altis/ uniquement
# ═══════════════════════════════════════════════════════════════
CORS_URLS_REGEX = r"^/api/altis/.*$"

CORS_ALLOWED_ORIGINS = env_list(
    "CORS_ORIGINS",
    "https://altisphere-group.com,"
    "https://www.altisphere-group.com,"
    "https://kshieldid-ai.github.io",
)
if DEBUG:
    CORS_ALLOWED_ORIGINS += [
        "http://localhost:8080",    # port reel du dev server Vite
        "http://127.0.0.1:8080",
        "http://localhost:5173",    # conserve si le port change
        "http://127.0.0.1:5173",
        "http://localhost:4173",    # npm run preview
    ]

CORS_ALLOW_CREDENTIALS = False
CORS_ALLOW_METHODS = ["GET", "POST", "OPTIONS"]
CORS_ALLOW_HEADERS = ["accept", "content-type", "origin"]
CORS_PREFLIGHT_MAX_AGE = 86400

REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [],
    "DEFAULT_THROTTLE_RATES": {
        # Devis : engageant commercialement, quota serre
        "altis_devis": os.environ.get(
            "ALTIS_THROTTLE_DEVIS", "1000/hour" if DEBUG else "5/hour"
        ),
        # Contact : un visiteur peut legitimement ecrire plusieurs fois
        "altis_contact": os.environ.get(
            "ALTIS_THROTTLE_CONTACT", "1000/hour" if DEBUG else "10/hour"
        ),
    },
}

# ═══════════════════════════════════════════════════════════════
# EMAIL — piloté par EMAIL_MODE : console | file | mailpit | smtp
# ═══════════════════════════════════════════════════════════════
ALTIS_NOTIFY_EMAILS = env_list("ALTIS_NOTIFY_EMAILS", "support@altisphere-group.com")
DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL", "ALTIS SPHERE <no-reply@altisphere-group.com>"
)

EMAIL_MODE = os.environ.get("EMAIL_MODE", "console").strip().lower()

if EMAIL_MODE == "console":
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

elif EMAIL_MODE == "file":
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = BASE_DIR / "tmp" / "emails"
    os.makedirs(EMAIL_FILE_PATH, exist_ok=True)

elif EMAIL_MODE == "mailpit":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "127.0.0.1"
    EMAIL_PORT = 1025
    EMAIL_USE_TLS = False
    EMAIL_USE_SSL = False
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""
    EMAIL_TIMEOUT = 10

elif EMAIL_MODE == "smtp":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
    EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
    EMAIL_USE_SSL = env_bool("EMAIL_USE_SSL", "False")
    EMAIL_USE_TLS = False if EMAIL_USE_SSL else env_bool("EMAIL_USE_TLS", "True")
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
    # Les mots de passe d'application Google s'affichent par groupes de 4
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "").replace(" ", "")
    EMAIL_TIMEOUT = 20

    _missing = [
        n for n in ("EMAIL_HOST", "EMAIL_HOST_USER", "EMAIL_HOST_PASSWORD")
        if not os.environ.get(n)
    ]
    if _missing:
        raise ImproperlyConfigured(
            f"EMAIL_MODE=smtp mais variables manquantes : {', '.join(_missing)}"
        )

else:
    raise ImproperlyConfigured(
        f"EMAIL_MODE='{EMAIL_MODE}' inconnu. "
        "Valeurs acceptées : console, file, mailpit, smtp."
    )
# SECURITY SETTINGS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_TRUSTED_ORIGINS = [
    "https://affagripel-lualaba.com",
    "https://www.affagripel-lualaba.com",
]


# from pathlib import Path
# import os

# from django.core.exceptions import ImproperlyConfigured
# from dotenv import load_dotenv

# BASE_DIR = Path(__file__).resolve().parent.parent

# # ⚠ override=True : le .env est la SOURCE DE VÉRITÉ.
# # Il écrase toute variable déjà posée dans le shell ($env: / export).
# load_dotenv(BASE_DIR / ".env", override=True)


# def env_bool(name, default="False"):
#     return os.environ.get(name, default).strip().lower() in ("true", "1", "yes")


# def env_list(name, default=""):
#     return [v.strip() for v in os.environ.get(name, default).split(",") if v.strip()]


# # ═══════════════════════════════════════════════════════════════
# # SÉCURITÉ
# # ═══════════════════════════════════════════════════════════════
# SECRET_KEY = os.environ.get(
#     "DJANGO_SECRET_KEY",
#     "c%+_15#vjbllro0m%ywym!eapupmdy8^l3t@iv3jyjcea=$x*o",  # fallback dev
# )
# DEBUG = env_bool("DJANGO_DEBUG", "False")
# ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")

# SESSION_ENGINE = "django.contrib.sessions.backends.db"

# # ═══════════════════════════════════════════════════════════════
# # APPLICATIONS
# # ═══════════════════════════════════════════════════════════════
# INSTALLED_APPS = [
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",
#     "core",
#     "tailwind",
#     "corsheaders",
#     "rest_framework",
#     "altis",
# ]

# # ⚠ CorsMiddleware DOIT être en position 1, avant SecurityMiddleware.
# MIDDLEWARE = [
#     "corsheaders.middleware.CorsMiddleware",
#     "django.middleware.security.SecurityMiddleware",
#     "whitenoise.middleware.WhiteNoiseMiddleware",
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]

# ROOT_URLCONF = "affagripelderu.urls"
# WSGI_APPLICATION = "affagripelderu.wsgi.application"

# TEMPLATES = [
#     {
#         "BACKEND": "django.template.backends.django.DjangoTemplates",
#         "DIRS": [BASE_DIR / "templates"],
#         "APP_DIRS": True,
#         "OPTIONS": {
#             "context_processors": [
#                 "django.template.context_processors.request",
#                 "django.contrib.auth.context_processors.auth",
#                 "django.contrib.messages.context_processors.messages",
#             ],
#         },
#     },
# ]

# # ═══════════════════════════════════════════════════════════════
# # BASE DE DONNÉES
# # ═══════════════════════════════════════════════════════════════
# if os.environ.get("ENVIRONMENT") == "production":
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql",
#             "NAME": os.environ.get("DB_NAME", "affagripel"),
#             "USER": os.environ.get("DB_USER", "django_user"),
#             "PASSWORD": os.environ.get("DB_PASSWORD", ""),
#             "HOST": os.environ.get("DB_HOST", "localhost"),
#             "PORT": os.environ.get("DB_PORT", "5432"),
#         }
#     }
# else:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": BASE_DIR / "db.sqlite3",
#         }
#     }

# AUTH_PASSWORD_VALIDATORS = [
#     {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
#     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
#     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
#     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
# ]

# LANGUAGE_CODE = "fr"
# TIME_ZONE = "Africa/Lubumbashi"
# USE_I18N = True
# USE_TZ = True

# STATIC_URL = "/static/"
# STATIC_ROOT = BASE_DIR / "static"
# MEDIA_URL = "/media/"
# MEDIA_ROOT = BASE_DIR / "media"

# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# # ═══════════════════════════════════════════════════════════════
# # ALTIS SPHERE — CORS scopé sur /api/altis/ uniquement
# # ═══════════════════════════════════════════════════════════════
# CORS_URLS_REGEX = r"^/api/altis/.*$"

# CORS_ALLOWED_ORIGINS = env_list(
#     "CORS_ORIGINS",
#     "https://altisphere-group.com,"
#     "https://www.altisphere-group.com,"
#     "https://kshieldid-ai.github.io",
# )
# if DEBUG:
#     CORS_ALLOWED_ORIGINS += ["http://localhost:5173", "http://127.0.0.1:5173"]

# CORS_ALLOW_CREDENTIALS = False
# CORS_ALLOW_METHODS = ["GET", "POST", "OPTIONS"]
# CORS_ALLOW_HEADERS = ["accept", "content-type", "origin"]
# CORS_PREFLIGHT_MAX_AGE = 86400

# REST_FRAMEWORK = {
#     "DEFAULT_THROTTLE_CLASSES": [],
#     "DEFAULT_THROTTLE_RATES": {
#         "altis_devis": os.environ.get("ALTIS_THROTTLE", "1000/hour" if DEBUG else "5/hour"),
#     },
# }

# # ═══════════════════════════════════════════════════════════════
# # EMAIL — piloté par EMAIL_MODE : console | file | mailpit | smtp
# # ═══════════════════════════════════════════════════════════════
# ALTIS_NOTIFY_EMAILS = env_list("ALTIS_NOTIFY_EMAILS", "support@altisphere-group.com")
# DEFAULT_FROM_EMAIL = os.environ.get(
#     "DEFAULT_FROM_EMAIL", "ALTIS SPHERE <no-reply@altisphere-group.com>"
# )

# EMAIL_MODE = os.environ.get("EMAIL_MODE", "console").strip().lower()

# if EMAIL_MODE == "console":
#     EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# elif EMAIL_MODE == "file":
#     EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
#     EMAIL_FILE_PATH = BASE_DIR / "tmp" / "emails"
#     os.makedirs(EMAIL_FILE_PATH, exist_ok=True)

# elif EMAIL_MODE == "mailpit":
#     EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
#     EMAIL_HOST = "127.0.0.1"
#     EMAIL_PORT = 1025
#     EMAIL_USE_TLS = False
#     EMAIL_USE_SSL = False
#     EMAIL_HOST_USER = ""
#     EMAIL_HOST_PASSWORD = ""
#     EMAIL_TIMEOUT = 10

# elif EMAIL_MODE == "smtp":
#     EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
#     EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
#     EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 465))
#     EMAIL_USE_SSL = env_bool("EMAIL_USE_SSL", "False")
#     EMAIL_USE_TLS = False if EMAIL_USE_SSL else env_bool("EMAIL_USE_TLS", "True")
#     EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
#     # Les mots de passe d'application Google s'affichent par groupes de 4
#     EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "").replace(" ", "")
#     EMAIL_TIMEOUT = 20

#     _missing = [
#         n for n in ("EMAIL_HOST", "EMAIL_HOST_USER", "EMAIL_HOST_PASSWORD")
#         if not os.environ.get(n)
#     ]
#     if _missing:
#         raise ImproperlyConfigured(
#             f"EMAIL_MODE=smtp mais variables manquantes : {', '.join(_missing)}"
#         )

# else:
#     raise ImproperlyConfigured(
#         f"EMAIL_MODE='{EMAIL_MODE}' inconnu. "
#         "Valeurs acceptées : console, file, mailpit, smtp."
#     )


# if DEBUG:
#     CORS_ALLOWED_ORIGINS += [
#         "http://localhost:8080",    # ← port réel de Vite (vite.config.ts)
#         "http://127.0.0.1:8080",
#         "http://localhost:5173",    # conservé au cas où le port change
#         "http://127.0.0.1:5173",
#         "http://localhost:4173",    # npm run preview
#     ]