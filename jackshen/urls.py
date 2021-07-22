import os

from django.conf.urls.static import static
from django.contrib import admin
from django.views.static import serve
from django.urls import path, include

from jackshen import settings
from jackshen.settings import BASE_DIR

urlpatterns = [
    path('', include("home.urls")),
    path('admin/', admin.site.urls),
    path('todo/', include('todo.urls', namespace='todo')),
    path('ip-locator/', include('ip_locator.urls', namespace='ip_locator')),
]

# Serve the favicon
urlpatterns += [
    path('favicon.ico', serve, {
        'path': 'favicon.ico',
        'document_root': os.path.join(BASE_DIR, 'home/static'),
    }
         ),
]

# Serve the media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
