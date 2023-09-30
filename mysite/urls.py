from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('dsfeke/', admin.site.urls),
    path('', include('base.urls.base_urls')),
    path('order/', include('base.urls.order_urls')),

    path('api/', include('product.api.urls')),

    path('product/', include('product.urls')),
    path('fetch/', include('base.urls.fetch_urls')),

    path('users/', include('users.urls.users_urls')),
    path('admin/', include('users.urls.admin_urls')),
    path('expert/', include('users.urls.expert_urls')),

    path('report/', include('base.urls.report_urls')),

    path('exhibition/', include('users.urls.exhibition_urls')),
    #
    # url(r'^media/(?P<path>.*)$', serve,
    #     {'document_root': settings.MEDIA_ROOT}),

    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}),
]
# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
