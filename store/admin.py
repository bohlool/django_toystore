from django.contrib import admin

from store.models import Category, ImageGallery, Product, VideoGallery, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')
    search_fields = ('name',)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class ImageGalleryInline(admin.TabularInline):
    model = ImageGallery
    extra = 1


class VideoGalleryInline(admin.TabularInline):
    model = VideoGallery
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [CommentInline, ImageGalleryInline, VideoGalleryInline]
    list_display = ('id', 'name', 'price', 'category', 'created', 'modified')
    search_fields = ('name', 'category', 'description')
    list_filter = ('category',)
    date_hierarchy = 'created'


@admin.register(ImageGallery)
class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image', 'created', 'modified')


@admin.register(VideoGallery)
class VideoGalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'video', 'created', 'modified')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'content', 'created', 'is_confirmed')
    search_fields = ('content',)
    list_filter = ('product', 'user__username', 'is_confirmed')
    date_hierarchy = 'created'
