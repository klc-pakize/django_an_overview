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

@api_view(['GET', 'POST'])
def article_list_create_api_view(request): 
    if request.method == 'GET':
        articles = Article.objects.filter(status = True)  # nesnelerden oluşan sorgu kümesi | queryset consisting of objects
        serializer = ArticleSerializer(articles, many=True)  # Many=True dedik çünkü birden fazla sorgu seti olabilir. | We said many=True because there may be more than one queryset.
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)