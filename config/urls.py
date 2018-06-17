from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from rest_framework.urlpatterns import format_suffix_patterns

from bootcamp.activities import views as activities_views
from bootcamp.authentication import views as bootcamp_auth_views
from bootcamp.core import views as core_views
from bootcamp.search import views as search_views

from rest_framework import routers
from bootcamp.api import views as api_views

# rest framework router
router = routers.DefaultRouter()
router.register(r'users', api_views.UserViewSet)
router.register(r'activities', api_views.GenericActivityListViewSet)
router.register(r'notifications', api_views.GenericNotificationListViewSet)
router.register(r'feeds', api_views.GenericFeedViewSet)
router.register(r'notifications', api_views.GenericNotificationViewSet)
router.register(r'articles', api_views.GenericArticleViewSet)
router.register(r'article-comments', api_views.GenericArticleCommentViewSet)
router.register(r'messages', api_views.GenericMessageViewSet)

urlpatterns = [
    # django rest framework routes
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/_users/$', api_views.user_list),
    url(r'^api/_users/(?P<pk>[0-9]+)/$', api_views.user_detail),

    # standard routes
    url(r'^$', core_views.home, name='home'),
    url(r'^login', auth_views.login, {'template_name': 'core/cover.html'},
        name='login'),
    url(r'^logout', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/$', bootcamp_auth_views.signup, name='signup'),
    url(r'^settings/$', core_views.settings, name='settings'),
    url(r'^settings/picture/$', core_views.picture, name='picture'),
    url(r'^settings/upload_picture/$', core_views.upload_picture,
        name='upload_picture'),
    url(r'^settings/save_uploaded_picture/$', core_views.save_uploaded_picture,
        name='save_uploaded_picture'),
    url(r'^settings/password/$', core_views.password, name='password'),
    url(r'^network/$', core_views.network, name='network'),
    url(r'^feeds/', include('bootcamp.feeds.urls')),
    url(r'^articles/', include('bootcamp.articles.urls')),
    url(r'^messages/', include('bootcamp.messenger.urls')),
    url(r'^notifications/$', activities_views.notifications,
        name='notifications'),
    url(r'^notifications/last/$', activities_views.last_notifications,
        name='last_notifications'),
    url(r'^notifications/check/$', activities_views.check_notifications,
        name='check_notifications'),
    # For autocomplete suggestions
    url(r'^autocomplete/$',
        search_views.get_autocomplete_suggestions, name='autocomplete'),
    url(r'^search/$', search_views.search, name='search'),
    url(r'^(?P<username>[^/]+)/$', core_views.profile, name='profile'),
    url(r'^i18n/', include('django.conf.urls.i18n', namespace='i18n')),
    url(r'^upload/', include('django_file_form.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
