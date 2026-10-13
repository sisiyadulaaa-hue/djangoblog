
from django.urls import path
from . import views


urlpatterns = [

    # Home page
    path(
        '',
        views.post_list,
        name='home'
    ),

    # User Login
    path(
        'login/',
        views.UserLoginView.as_view(),
        name='login'
    ),

    # User Logout
    path(
        'logout/',
        views.UserLogoutView.as_view(),
        name='logout'
    ),

    # My Posts
    path(
        'my-posts/',
        views.MyPostsView.as_view(),
        name='my_posts'
    ),

    # User Registration
    path(
        'register/',
        views.RegisterView.as_view(),
        name='register'
    ),

    # Create a post
    path(
        'posts/new/',
        views.PostCreateView.as_view(),
        name='post_create'
    ),

    # Edit a post
    path(
        'posts/<slug:slug>/edit/',
        views.PostUpdateView.as_view(),
        name='post_edit'
    ),

    # Delete a post
    path(
        'posts/<slug:slug>/delete/',
        views.PostDeleteView.as_view(),
        name='post_delete'
    ),

    # Delete a comment
    path(
        'comments/<int:comment_id>/delete/',
        views.delete_comment,
        name='delete_comment'
    ),

    # Post detail
    path(
        'posts/<slug:slug>/',
        views.post_detail,
        name='post_detail'
    ),

    # About page
    path(
        'about/',
        views.about,
        name='about'
    ),

    # Contact page
    path(
        'contact/',
        views.contact,
        name='contact'
    ),

]

