
from django.contrib import admin
from django.contrib.auth import urls as auth_urls
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from material.frontend import urls as frontend_urls

from zite.views import *
_urlpatterns = [
    # path('', BidView.as_view()),
    path('tgbotwebhook/', csrf_exempt(BotWebHook.as_view())),

    # path('buttonsets/', ButtonSetListView.as_view()),
    path('admin/', admin.site.urls),
    path('accounts/', include(auth_urls)),
]

urlpatterns = [
    path('xcs/', include(_urlpatterns))
]
