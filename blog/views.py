from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Post


def home(request):

    posts = Post.objects.all()

    return render(request, 'blog/home.html', {'posts': posts})


def about(request):

    return render(request, 'blog/about.html')


def contact(request):

    return render(request, 'blog/contact.html', {'abc': 'D'})


def post_list(request):

    posts = Post.objects.filter(status="published").order_by("-created_at")

    paginator = Paginator(posts, 6)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(request, "blog/post_list.html", {
        "page_obj": page_obj
    })


def post_detail(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug,
        status="published"
    )

    return render(request, "blog/post_detail.html", {
        "post": post
    })

class PostCreateView(CreateView):
    model = Post
    fields = ["title", "content", "category", "tags", "status"]
    template_name = "blog/post_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "post_detail",
            kwargs={"slug": self.object.slug}
        )

class PostUpdateView(UpdateView):
    model = Post
    fields = ["title", "content", "category", "tags", "status"]
    template_name = "blog/post_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "post_detail",
            kwargs={"slug": self.object.slug}
        )

class PostDeleteView(DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("home")