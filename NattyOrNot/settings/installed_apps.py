INSTALLED_APPS = [
    # my apps
    'users',
    'training',
    'dashboard',
    # django defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # cors headers
    'corsheaders',
    # rest framework
    'rest_framework',
    # all auth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # disqus
    'disqus',
    # debug toolbar
    'debug_toolbar',
    # axes
    'axes',
]
