from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('board.views',
    url(r'^$', 'home', name = 'home'),
    url(r'^board/(\w+)/$', 'show_board', name = 'show_board'),
)
