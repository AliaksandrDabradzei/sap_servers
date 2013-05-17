from django.conf.urls.defaults import *  # @UnusedWildImport
# from mysite import views
# from mysite.books import views

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('mysite.views',
    (r'^hello/$', 'hello')
    ('^time/$', 'current_datetime'),
    (r'^time/plus/(\d{1,2})/$', 'hours_ahead'),


#    (r'^search-form/$', views.search_form),
#    (r'^search/$', views.search),
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
#    (r'^admin/', include(admin.site.urls)),
)
