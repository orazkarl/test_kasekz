from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, Comment
from .forms import PostForm, CommentForm


class IndexView(generic.ListView):
    template_name = 'mainapp/index.html'
    model = Post


class PostDetailView(generic.TemplateView):
    template_name = 'mainapp/post_detail.html'

    def get(self, request, *args, **kwargs):
        comment_form = CommentForm()
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        allcomments = post.comments.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(allcomments, 10)
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
        self.extra_context = {
            'post': post,
            'comments': comments,
            'comment_form': comment_form,
            'allcomments': allcomments,
        }
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        user = request.user
        parent_id = request.POST['parent']
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            if parent_id:
                parent = get_object_or_404(Comment, id=parent_id)
                user_comment.parent = parent
            user_comment.post = post
            user_comment.user = user
            user_comment.save()

        return redirect('/post/detail/' + str(post.id))


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

class CommentDeleteView(generic.DeleteView):
    model = Comment

    def get_success_url(self, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs['pk'])
        post_id = comment.post.id
        return reverse('post_detail', kwargs={'pk': post_id})

    def get(self, request, *args, **kwargs):
        print(self.kwargs['pk'])
        return self.post(request, *args, **kwargs)

class CommentUpdateView(generic.UpdateView):
    model = Comment
    form_class = CommentForm

    def get_success_url(self, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs['pk'])
        post_id = comment.post.id
        return reverse('post_detail', kwargs={'pk': post_id})