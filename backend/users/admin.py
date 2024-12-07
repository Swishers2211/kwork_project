from django.contrib import admin

from users.models import (
    User, 
    Subscription,
    Interests,
    Friendship,
)

admin.site.register(Friendship)
admin.site.register(Subscription)
admin.site.register(User)
admin.site.register(Interests)
