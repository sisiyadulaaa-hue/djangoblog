from django.urls import path
from django.contrib.auth import views as auth_views
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

# Password Reset
path(
    'password-reset/',
    auth_views.PasswordResetView.as_view(
        template_name='blog/password_reset.html',
        email_template_name='blog/password_reset_email.html',
        subject_template_name='blog/password_reset_subject.txt',
        success_url='/password-reset/done/'
    ),
    name='password_reset'
),

path(
    'password-reset/done/',
    auth_views.PasswordResetDoneView.as_view(
        template_name='blog/password_reset_done.html'
    ),
    name='password_reset_done'
),

path(
    'reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name='blog/password_reset_confirm.html'
    ),
    name='password_reset_confirm'
),

path(
    'reset/done/',
    auth_views.PasswordResetCompleteView.as_view(
        template_name='blog/password_reset_complete.html'
    ),
    name='password_reset_complete'
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
