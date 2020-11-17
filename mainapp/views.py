from django.shortcuts import render
from django.views import generic

from .models import Post
from .forms import PostForm

class IndexView(generic.ListView):
    template_name = 'mainapp/index.html'
    model = Post


class PostDetailView(generic.DetailView):
    model = Post

class PostCreateView(generic.CreateView):
    model = Post
    form_class = PostForm
    success_url = '/'
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super(PostCreateView, self).form_valid(form)

class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm
    success_url = '/'

class PostDeleteView(generic.DeleteView):
    model = Post
    success_url = '/'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)