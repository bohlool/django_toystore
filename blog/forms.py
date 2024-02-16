from django import forms
from django.urls import reverse_lazy

from .models import Post, Comment


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if visible.field.label == 'Subject':
                visible.field.widget.attrs['class'] = 'form-control subject-auto-complete'
                visible.field.widget.attrs['autocomplete'] = 'off'
                visible.field.widget.attrs['data-url'] = reverse_lazy('subject_auto_complete')

    class Meta:
        model = Post
        fields = ('title', 'subject', 'text',)


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Comment
        fields = ('text',)
