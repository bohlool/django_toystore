from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'imagegallery', views.ImageGalleryViewSet)
router.register(r'videogallery', views.VideoGalleryViewSet)
router.register(r'product-comments', views.CommentViewSet)

urlpatterns = [
    path('api', include(router.urls)),
    path('', views.CategoryListView.as_view(), name='store'),
    path('categories/<int:category_id>/products/', views.ProductListView.as_view(), name='product-list-by-category'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/comment/', views.CommentCreateView.as_view(), name='add-comment'),
]
