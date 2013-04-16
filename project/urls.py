from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

baseurl = 'kittens/'

urlpatterns = patterns('',
    url(r'^%s?$' % baseurl, 'kittens.views.index'),
    url(r'^%sfetch$' % baseurl, 'kittens.views.fetch_image'),
    url(r'^%s(?P<width>\d+)/(?P<height>\d+)/?$' % baseurl, 'kittens.views.kitten'),
    url(r'^%s(?P<width>\d+)/(?P<height>\d+)/js$' % baseurl, 'kittens.views.kitten_js'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

