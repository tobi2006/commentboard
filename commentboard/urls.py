from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('board.views',
    url(r'^$', 'home', name = 'set_up_board'),
    url(r'^board/(\w+)/$', 'show_board', name = 'show_board'),
    url(r'^vote_up/(\d+)/$', 'vote_up', name = 'vote_up'),
    url(r'^vote_down/(\d+)/$', 'vote_down', name = 'vote_down')
)
