from django.contrib import admin

from users.models import (
    User, 
    Subscription,
    Interests,
)
admin.site.register(Subscription)
admin.site.register(User)
admin.site.register(Interests)
