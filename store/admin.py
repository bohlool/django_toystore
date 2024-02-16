from django.contrib import admin

from store.models import Category, ImageGallery, Product, VideoGallery, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ('name', 'price', 'category')


@admin.register(ImageGallery)
class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')


@admin.register(VideoGallery)
class VideoGalleryAdmin(admin.ModelAdmin):
    list_display = ('product', 'video')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'content')
