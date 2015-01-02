from django.conf.urls import patterns, include, url
from django.contrib import admin
from new_soycorn import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='index'),
    url(r'^article/(?P<article_id>\d+)/$', views.article, name='article'),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
