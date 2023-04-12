import re
from django.contrib import admin
from django.urls import path
from django.urls.conf import include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('api/v1/tickets/', include('apps.request.urls')),
    path('api/v1/admin/', admin.site.urls),

]

kwargs = {"document_root": settings.STATIC_ROOT}
urlpatterns.append(re_path(r"^%s(?P<path>.*)$" % re.escape(settings.STATIC_URL.lstrip("/")), serve, kwargs=kwargs))
