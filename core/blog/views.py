from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm
from .models import Post


# Create your views here.

class IndexTemplateView(TemplateView):
    """
    Class Based View (TemplateView) to show index page.
    """

    template_name = 'index.html'
    extra_context = {'name': 'FAroogh'}

    def get_context_data(self, **kwargs):
        context = super(IndexTemplateView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context


class MaktabRedirectView(RedirectView):
    """
    Class Based View (RedirectView) for Provide a redirect on any GET request with
    URL address or Pattern name.
    """
    url = 'https://maktabkhooneh.org/'


class PostListView(ListView):
    """
    Render some Blog Post list of objects, set by `self.model` or `self.queryset`.
    `self.queryset` can actually be any iterable of items, not just a queryset.
    """

    model = Post
    # queryset = Post.objects.filter(status=True)
    context_object_name = 'posts'
    ordering = '-published_date'
    paginate_by = 3

    # def get_queryset(self):
    #     posts = Post.objects.filter(author=4)
    #     return posts


class PostDetailView(LoginRequiredMixin, DetailView):
    """
    Render a "detail" view of a Post object.

    By default, this is a model instance looked up from `self.queryset`, but the
    view will support display of *any* object by overriding `self.get_object()`.
    """

    model = Post
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'


class PostCreateView(CreateView):
    """
    View for creating a new Post object, with a response rendered by a template.
    """

    model = Post
    form_class = PostForm
    success_url = '/blog/posts/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(UpdateView):
    """
    View for updating a Post object, with a response rendered by a template.
    """

    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:post-list')


class PostDeleteView(DeleteView):
    """
    View for deleting a Post object retrieved with self.get_object(), with a
    response rendered by a template.
    """

    model = Post
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:post-list')
