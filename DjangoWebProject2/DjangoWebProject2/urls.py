"""
Definition of urls for DjangoWebProject2.
"""

from datetime import datetime
from django.conf.urls import url,include
import django.contrib.auth.views

import app.forms
import app.views

from django.views.static import serve
from django.conf import settings

from django.conf.urls.static import static



# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()
urlpatterns = [url(r'^OverDueRemind/', include('app.appurls')),
    url(r'^', include('app.appurls')),]
urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


