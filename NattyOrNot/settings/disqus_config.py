from os import environ

# disqus config

DISQUS_API_KEY = environ.get('DISQUS_SECRET_KEY', '')
DISQUS_WEBSITE_SHORTNAME = environ.get('DISQUS_WEBSITE_SHORTNAME', '')
