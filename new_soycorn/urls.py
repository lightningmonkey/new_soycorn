from django.conf.urls import patterns, include, url
from django.contrib import admin
from new_soycorn import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^article/(\d+)$', views.article_single, name='article_single'),
                       url(r'^article/page/(\d+)$', views.article_page, name='article_page'),
                       url(r'^faq$', views.faq, name='faq'),
                       url(r'^contact-us$', views.contact_us, name='contact_us'),
                       url(r'^about-us$', views.about_us, name='about_us'),
                       url(r'^pdf-view$', views.pdf_view, name='pdf_view'),

                       url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
