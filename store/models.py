from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

User = get_user_model()


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    is_active = models.BooleanField(default=True)
    featured_image = models.FileField(blank=True, null=True, upload_to='store/products/img/featured/',
                                      validators=[
                                          FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])])

    def __str__(self):
        return self.name


class ImageGallery(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.FileField(upload_to='store/products/img/',
                             validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])])

    def __str__(self):
        return self.image.name


class VideoGallery(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='store/products/video/',
                             validators=[FileExtensionValidator(allowed_extensions=['mp4'])])

    def __str__(self):
        return self.video.name


class Comment(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_comments')
    content = models.TextField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.content
