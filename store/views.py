from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response

from blog.permissions import IsOwnerOrSuperuser
from store.models import Category, Product, Comment, ImageGallery, VideoGallery
from store.serializers import CategorySerializer, ProductSerializer, ImageGallerySerializer, CommentSerializer, \
    VideoGallerySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    @action(detail=True)
    def comments(self, request, *args, **kwargs):
        product = self.get_object()
        return Response(CommentSerializer(product.comments.filter(is_confirmed=True), many=True).data)

    @action(detail=True)
    def images(self, request, *args, **kwargs):
        product = self.get_object()
        return Response(ImageGallerySerializer(product.images.all(), many=True).data)

    @action(detail=True)
    def videos(self, request, *args, **kwargs):
        product = self.get_object()
        return Response(VideoGallerySerializer(product.videos.all(), many=True).data)


class ImageGalleryViewSet(viewsets.ModelViewSet):
    queryset = ImageGallery.objects.all()
    serializer_class = ImageGallerySerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class VideoGalleryViewSet(viewsets.ModelViewSet):
    queryset = VideoGallery.objects.all()
    serializer_class = VideoGallerySerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(is_confirmed=True)
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrSuperuser]
    search_fields = ['user__username', 'text']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_confirmed=True)
        context['images'] = self.object.images.all()
        context['videos'] = self.object.videos.all()
        return context


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
