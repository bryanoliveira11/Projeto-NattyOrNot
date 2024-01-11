MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # my middlewares
    'users.notifications_middleware.NotificationsMiddleware',
    # cors headers middleware
    'corsheaders.middleware.CorsMiddleware',
    # all auth middleware
    'allauth.account.middleware.AccountMiddleware',
    # debug toolbar middleware
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # AxesMiddleware should be the last middleware in the MIDDLEWARE list.
    'axes.middleware.AxesMiddleware',
]
