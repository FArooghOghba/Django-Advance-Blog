from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):
    """
    Class for creating post form.
    """

    class Meta:
        model = Post
        fields = ('title', 'content', 'category', 'status', 'published_date')

