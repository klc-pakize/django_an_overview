"""
APIViews: DRF, APIViews oluşturmak için 2 seçenek sunar:
1- @api_view decarator (Fonksiyon Tabanlı Görünüm)
2- APIView Classes

Bu yapılar sayesinde sunucumuza gönderilen istek veya cevapları kontrol etmemizi sağlar.

"Browsable API": Bir HTML arayüzü yazmadan API istekleri yapmak için kullanılan bir araçtır.

APIViews: DRF provides 2 options for creating APIViews:
1- @api_view decarator (Function Based View)
2- APIView Classes

Thanks to these structures, it allows us to control the requests or responses sent to our server.

"Browsable API": It is a tool to make API requests without writing an HTML interface.
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from news.models import Article
from .serializers import ArticleSerializer

@api_view(['GET'])
def article_list_create_api_view(request): 
    articles = Article.objects.filter(status = True)  # nesnelerden oluşan sorgu kümesi | queryset consisting of objects
    serializer = ArticleSerializer(articles)
    return Response(serializer.data)