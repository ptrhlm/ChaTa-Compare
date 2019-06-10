import os


def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


def getenv_required(var_name: str) -> str:
    result = os.getenv(var_name)
    assert result, f"Missing environment variable: {var_name}"
    return result


API_V1_STR = "/api/v1"

SECRET_KEY = os.getenvb(b"SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = os.urandom(32)

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days

SERVER_NAME = getenv_required("SERVER_NAME")
SERVER_HOST = os.getenv("SERVER_HOST")
BACKEND_CORS_ORIGINS = os.getenv(
    "BACKEND_CORS_ORIGINS"
)
# a string of origins separated by commas, e.g:
# "http://localhost, http://localhost:8080, http://local.dockertoolbox.tiangolo.com"

PROJECT_NAME = getenv_required("PROJECT_NAME")
SENTRY_DSN = os.getenv("SENTRY_DSN")

POSTGRES_SERVER = getenv_required("POSTGRES_SERVER")
POSTGRES_USER = getenv_required("POSTGRES_USER")
POSTGRES_PASSWORD = getenv_required("POSTGRES_PASSWORD")
POSTGRES_DB = getenv_required("POSTGRES_DB")
SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
)

SMTP_TLS = getenv_boolean("SMTP_TLS", True)
SMTP_PORT = None
_SMTP_PORT = os.getenv("SMTP_PORT")
if _SMTP_PORT is not None:
    SMTP_PORT = int(_SMTP_PORT)
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAILS_FROM_EMAIL = os.getenv("EMAILS_FROM_EMAIL")
EMAILS_FROM_NAME = PROJECT_NAME
EMAIL_RESET_TOKEN_EXPIRE_HOURS = 48
EMAIL_TEMPLATES_DIR = "/app/app/email-templates/build"
EMAILS_ENABLED = SMTP_HOST and SMTP_PORT and EMAILS_FROM_EMAIL

FIRST_SUPERUSER = os.getenv("FIRST_SUPERUSER")
FIRST_SUPERUSER_PASSWORD = os.getenv("FIRST_SUPERUSER_PASSWORD")

USERS_OPEN_REGISTRATION = getenv_boolean("USERS_OPEN_REGISTRATION")

MINIO_SERVER = 'storage:9000'
MINIO_BUCKET = getenv_required('MINIO_BUCKET')
MINIO_ACCESS_KEY = getenv_required('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = getenv_required('MINIO_SECRET_KEY')

REMOTE_AUTH_ENDPOINT = 'http://3.122.251.13/api/users/login'
