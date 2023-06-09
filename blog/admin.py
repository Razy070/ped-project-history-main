from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from django import forms
from .models import Comment, Post, PostRatingModel, Profile


class PostAdmin(SummernoteModelAdmin):
    list_display = ("title", "status", "created_on")
    list_filter = ("status", "created_on")
    search_fields = ["title", "content"]
    # prepopulated_fields = {"id": ("title",)}
    # summernote_fields = ("content",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "body", "post", "created_on", "active")
    list_filter = ("active", "created_on")
    search_fields = ("name", "email", "body")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(Post, PostAdmin)
admin.site.register(Profile)

admin.site.register(PostRatingModel)
