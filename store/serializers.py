from rest_framework import serializers

from store.models import Category, Product, ImageGallery, VideoGallery, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'category')


class ImageGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageGallery
        fields = ('id', 'product', 'image')


class VideoGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoGallery
        fields = ('id', 'product', 'video')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'product', 'user', 'content')
