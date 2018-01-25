
from django.contrib import admin

from zite import models

for m in models.__all__:
    admin.site.register(getattr(models, m))
