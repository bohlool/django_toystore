from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from rest_framework import viewsets

from store.models import Category, Product, ImageGallery, VideoGallery, Comment
from store.serializers import CategorySerializer, ProductSerializer, ImageGallerySerializer, CommentSerializer, \
    VideoGallerySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ImageGalleryViewSet(viewsets.ModelViewSet):
    queryset = ImageGallery.objects.all()
    serializer_class = ImageGallerySerializer


class VideoGalleryViewSet(viewsets.ModelViewSet):
    queryset = VideoGallery.objects.all()
    serializer_class = VideoGallerySerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CategoryListView(ListView):
    model = Category
    template_name = 'store/category_list.html'
    context_object_name = 'categories'


class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return Product.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'


class CommentCreateView(CreateView):
    model = Comment
    fields = ['content']
    template_name = 'store/add_comment.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = get_object_or_404(Product, pk=self.kwargs['product_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product-detail', kwargs={'pk': self.kwargs['product_id']})
