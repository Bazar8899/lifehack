from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from django.conf.urls.static import static
from django.conf import settings
from lifeHack.views import (index)

urlpatterns = [
    path('index/', index, name='main-view'),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('story/', include('story.urls')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
    
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)