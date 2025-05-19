from django.urls import path
from .views import (registerView,loginView,logoutView,homeView,CreatePostView,
comment,profile,follow,like_post,update_profile,post_delete_view)

urlpatterns=[
path("", homeView.as_view(), name="home"),
path("register/", registerView, name='register'),
path("login/", loginView, name="login"),
path("logout/", logoutView, name="logout"),


path("create-post/",CreatePostView , name="create-post"),
path("post/<int:pk>/",comment, name="post-detail"),
path("profile/<int:user_id>", profile, name="profile"),
path("update-profile/", update_profile, name="update-profile"),
path("follow-user/<int:user_id>/", follow, name="follow"),
path("like/<int:post_id>/", like_post, name="like"),

path("post/delete/<int:post_id>/", post_delete_view, name="delete-post")

]