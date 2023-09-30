from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
                         # <-- The `name` we used to in the `DEFAULT_HOST` setting
                         host(r'www', settings.ROOT_URLCONF, name='www'),
                         host(r'exhibition', 'exhibition.urls',
                              name='exhibition'),
                         )
