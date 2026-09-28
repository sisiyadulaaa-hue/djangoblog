from django.urls import path

from . import views

urlpatterns = [

    path('', views.post_list, name='home'),

    path('posts/new/', views.PostCreateView.as_view(), name='post_create'),

    path('posts/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_edit'),

    path('posts/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),

    path('about/', views.about, name='about'),

    path('contact/', views.contact, name='contact'),

]