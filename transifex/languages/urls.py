from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from models import Language
from feeds import AllLanguages, LanguageReleaseFeed
from views import (language_detail, slug_feed,
                   language_release, language_release_feed,
                   language_release_download)

admin.autodiscover()

feeds = {
    'all': AllLanguages,
    'language_release': LanguageReleaseFeed,
}

#TODO: Temporary until we import view from a common place
SLUG_FEED = 'languages.views.slug_feed'
urlpatterns = patterns('',
    url(
        regex = r'^feed/$',
        view = SLUG_FEED,
        name = 'languages_latest_feed',
        kwargs = {'feed_dict': feeds,
                  'slug': 'all'}),
    url(
        regex = '^(?P<language_slug>[-_@\w]+)/collection/(?P<collection_slug>[-\w]+)/(?P<release_slug>[-\w]+)/feed/$',
        view = language_release_feed,
        name = 'language_release_feed',
        kwargs = {'feed_dict': feeds,
                  'slug': 'language_release'}),
)


urlpatterns += patterns('django.views.generic',
    url (
        name = 'language_list',
        regex = '^$',
        view = 'list_detail.object_list',
        kwargs = {"template_object_name" : "language",
                  'queryset': Language.objects.all()}
    ),
    url(
        name = 'language_detail',
        regex = '^(?P<slug>[-_@\w]+)/$',
        view = language_detail,
        kwargs = {'slug_field': 'code',
                  "template_object_name" : "language",
                  'queryset': Language.objects.all()}
    ),
    url(
        name = 'language_release',
        regex = '^(?P<slug>[-_@\w]+)/collection/(?P<collection_slug>[-\w]+)/(?P<release_slug>[-\w]+)/$',
        view = language_release,
    ),
)

#TODO: Make this setting work throughout the applications
if getattr(settings, 'ENABLE_COMPRESSED_DOWNLOAD', True):
    urlpatterns += patterns('',
        url(
            name = 'language_release_download',
            regex = '^(?P<slug>[-_@\w]+)/collection/(?P<collection_slug>[-\w]+)/(?P<release_slug>[-\w]+)/download_(?P<filetype>[\w]+)/$',
            view = language_release_download,
        ),
)
