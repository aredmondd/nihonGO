from django.urls import path, include
from . import views
from .views import profile, ChangePasswordView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.my_login, name="login"),
    path('register/', views.register, name="register"),
    path('about/', views.about, name="about"),
    path('my-profile/', views.profile, name="my-profile"),
    path('edit-profile/', views.edit_profile, name="edit-profile"),
    path('mydecks/', views.my_decks, name="my_decks"),
    path('add/', views.add_deck, name='add_deck'),
    path('study/<int:deck_id>/', views.study, name='study'),
    path('user-logout', views.user_logout, name="user-logout"),
    path('profile/', profile, name='users-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='myapp/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='myapp/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='myapp/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='myapp/password_reset_complete.html'), name='password_reset_complete'),
    path('edit/<int:deck_id>/', views.edit_deck, name='edit_deck'),
    path('delete/<int:deck_id>/', views.delete_deck, name='delete_deck'),  
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forum/', views.forum_index, name='forum_index'),                   # List all posts
    path('forum/post/<int:post_id>/', views.post_detail, name='post_detail'),  # View a single post with replies
    path('forum/new/', views.create_post, name='create_post'),             # Create a new post
    path('forum/post/<int:post_id>/reply/', views.add_reply, name='add_reply'), # Add a reply to a post
    path('upvote/<int:post_id>/', views.upvote_post, name='upvote_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),  # Check that 'post_detail' is correctly defined
    path('deck/<int:deck_id>/add_cards/', views.add_cards, name='add_cards'),
    path('update-progress/', views.update_progress, name='update_progress'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
