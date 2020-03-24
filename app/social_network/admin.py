from django.contrib import admin

from app.social_network.models import Bot, Like, Post

admin.site.register(Post)
admin.site.register(Like)


class BotAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    ordering = ("created_at",)


admin.site.register(Bot, BotAdmin)
