from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.views.static import serve
from django.urls import re_path
from django.conf.urls.static import static

# Redirect root URL only once
urlpatterns = [
    path('', lambda request: redirect('/tet/')),  # Root redirect once only
]

# Linguistic URLs — everything with /tet/, /pt/, /en/ prefix
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('portal.urls')),
    path('kmbo/', include('main.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
)

# Static/media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

    
handler404 = "portal.views_error.error_404"
handler500 = "portal.views_error.error_500"
handler503 = "portal.views_error.error_503"
