import os

SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'django_nose',
    "tests",
    "contento"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CURRENT_DIR = os.path.dirname(__file__)
CONTENTO_FLATFILES_BASE =  os.path.abspath(os.path.join(CURRENT_DIR , "../contento/demo/demo/cms_pages"))

# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    '--cover-package=contento',
    '--with-coverage',
    '--nocapture',

]
