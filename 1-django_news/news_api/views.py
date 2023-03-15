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

from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
class ArticleAPIView(APIView):
    def get(self, request):
        articles = Article.objects.filter(status=True)
        serializer = ArticleSerializer(articles, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailAPIView(APIView):
    def get_obj(self, pk):
        article_instance = get_object_or_404(Article, pk = pk)
        return article_instance
    
    def get(self,request, pk):
        articles_instance = self.get_obj(pk=pk)
        serializer = ArticleSerializer(articles_instance)
        return Response(serializer.data)

    def put(self,request , pk):
        articles_instance = self.get_obj(pk=pk)
        serializer = ArticleSerializer(articles_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request , pk):
        articles_instance = self.get_obj(pk=pk)
        articles_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


########################## Function Based View ################################

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
    

@api_view(['GET', 'PUT', 'DELETE'])
def article_detail_list_api_view(request, pk): 
    try:
        article_instance = Article.objects.get(pk = pk)

    except Article.DoesNotExist:
        return Response(
           { "errors": {
                "code": 404,
                    "message":"There is no such article"
                }
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = ArticleSerializer(article_instance)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ArticleSerializer(article_instance, data= request.data)
        if serializer.is_valid():
            serializer.save
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        article_instance.delete()
        return Response(
           { "message": {
                "code": 204,
                    "message":"article deleted"
                }
            },
            status=status.HTTP_204_NO_CONTENT
        )
