from django.contrib import admin
from .models import Track, PrimaryAuthor, CoAuthor, Speaker, Abstract

# Register your models here.
admin.site.register(Track)
admin.site.register(PrimaryAuthor)
admin.site.register(CoAuthor)
admin.site.register(Speaker)
admin.site.register(Abstract)