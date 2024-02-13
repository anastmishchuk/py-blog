from django.contrib.auth import logout
from django.http import HttpRequest
from django.shortcuts import redirect
from django.views import generic
from blog.models import Post
from .forms import CommentForm


class IndexView(generic.ListView):
    model = Post
    template_name = "blog/index.html"
    queryset = (
        Post.objects.select_related("owner").prefetch_related("comments").
        order_by("-created_time"))
    paginate_by = 5


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


def add_comment(request: HttpRequest, post_id: int) -> redirect:
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = post_id
            comment.user = request.user
            comment.save()
    return redirect("blog:post-detail", pk=post_id)


def custom_logout(request) -> redirect:
    logout(request)
    return redirect("blog/logout/")