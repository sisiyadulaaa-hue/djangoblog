from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

import debug_toolbar


urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Blog Application
    path('', include('blog.urls')),

    # Django Debug Toolbar
    path('__debug__/', include(debug_toolbar.urls)),
]


# Media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )


# Custom 403 Permission Denied Page
handler403 = 'blog.views.permission_denied'