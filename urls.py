from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import settings
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CrazyLife.views.home', name='home'),
    # url(r'^CrazyLife/', include('CrazyLife.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url( r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT } ),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^edit-file/', 'live_edit.views.edit_file' ),
    url(r'^file-content/', 'live_edit.views.file_content' ),
)
