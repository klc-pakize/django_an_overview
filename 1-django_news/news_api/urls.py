from django.urls import path

from .views import article_list_create_api_view, article_detail_list_api_view, ArticleAPIView,ArticleDetailAPIView, JournalistAPIView,JournalistDetailAPIView

urlpatterns = [
    # path("articles", article_list_create_api_view, name="article-list"),
    # path("articles/<int:pk>/", article_detail_list_api_view, name="article-detail"),
    
    path("articles", ArticleAPIView.as_view()),
    path("articles/<int:pk>/", ArticleDetailAPIView.as_view()),
    path("journalist", JournalistAPIView.as_view()),
    path("journalist/<int:pk>/", JournalistDetailAPIView.as_view()),
]
