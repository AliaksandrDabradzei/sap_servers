from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'hosts/$', 'mysite.sap_servers.views.hosts_detail'),
)
