
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseForbidden

from .models import Post, Category, Comment
from .forms import PostForm, RegisterForm, CommentForm


# Home page
def home(request):
    posts = Post.objects.all().order_by("-created_at")

    return render(
        request,
        "blog/home.html",
        {"posts": posts}
    )


# About page
def about(request):
    return render(request, "blog/about.html")


# Contact page
def contact(request):
    return render(
        request,
        "blog/contact.html",
        {"abc": "D"}
    )


# Display published posts with pagination and filters
def post_list(request):
    posts = Post.objects.filter(
        status="published"
    ).order_by("-created_at")

    category_id = request.GET.get("category")
    tag_id = request.GET.get("tag")

    if category_id:
        posts = posts.filter(category_id=category_id)

    if tag_id:
        posts = posts.filter(tags__id=tag_id).distinct()

    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    categories = Category.objects.all()

    return render(
        request,
        "blog/post_list.html",
        {
            "page_obj": page_obj,
            "categories": categories,
        }
    )


# Post detail and comments
def post_detail(request, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        status="published"
    )

    comments = post.comments.select_related(
        "author"
    ).order_by("-created_at")

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            return redirect(
                "post_detail",
                slug=post.slug
            )
    else:
        form = CommentForm()

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_form": form,
        }
    )


# Delete comment (owner only)
def delete_comment(request, comment_id):
    if not request.user.is_authenticated:
        return redirect("login")

    comment = get_object_or_404(
        Comment,
        id=comment_id
    )

    # Only the comment owner can delete it
    if comment.author != request.user:
        return HttpResponseForbidden(
            "You can only delete your own comments."
        )

    # Delete only through POST requests
    if request.method == "POST":
        post_slug = comment.post.slug
        comment.delete()

        return redirect(
            "post_detail",
            slug=post_slug
        )

    return redirect(
        "post_detail",
        slug=comment.post.slug
    )


# Register
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "blog/register.html"
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


# Create post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "post_detail",
            kwargs={"slug": self.object.slug}
        )


# Edit post (owner only)
class PostUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def get_success_url(self):
        return reverse_lazy(
            "post_detail",
            kwargs={"slug": self.object.slug}
        )


# Delete post (owner only)
class PostDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("home")
    login_url = "login"

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


# Login
class UserLoginView(LoginView):
    template_name = "blog/login.html"
    redirect_authenticated_user = True


# Logout
class UserLogoutView(LogoutView):
    next_page = "home"


# My Posts (show only the logged-in user's posts)
class MyPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/my_posts.html"
    context_object_name = "posts"
    paginate_by = 6
    login_url = "login"

    def get_queryset(self):
        return Post.objects.filter(
            author=self.request.user
        ).order_by("-created_at")

# Custom 403 Permission Denied Page
def permission_denied(request, exception=None):
    return render(
        request,
        "blog/403.html",
        status=403
    )