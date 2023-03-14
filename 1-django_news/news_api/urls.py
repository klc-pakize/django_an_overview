from django.urls import path

from .views import article_list_create_api_view

urlpatterns = [
    path("articles", article_list_create_api_view, name="article-list")
]
