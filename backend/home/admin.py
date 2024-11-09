from django.contrib import admin

from home.models import (
    Video,
    CategoryVideo,
    Comment,
)

admin.site.register(Comment)
admin.site.register(CategoryVideo)
admin.site.register(Video)
