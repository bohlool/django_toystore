from django.contrib import admin

from .models import Post, Comment, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


class CommentInlineAdmin(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ('user', 'date', 'text', 'is_confirmed')
    readonly_fields = ('date',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInlineAdmin]
    list_display = ('id', 'title', 'subject', 'user', 'date')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'subject', 'text')
    list_filter = ('subject', 'user', 'date')
    date_hierarchy = 'date'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'date', 'text', 'is_confirmed')
    list_display_links = ('id', 'post')
    search_fields = ('text',)
    list_filter = ('user', 'date', 'is_confirmed')
    date_hierarchy = 'date'
