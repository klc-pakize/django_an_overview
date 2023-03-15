from rest_framework import serializers

from django.utils.timesince import timesince

from datetime import datetime, date

from news.models import Article, Journalist

#? Serializer = karmaşık yapıları (JSON, XML vb.) backend olarak kullandığımız python veri yapılarına (dic, tuple, list, set) dönüştürür. Her iki şekilde de çalışır.
#? Serializer = converts complex structures (JSON, XML etc.) to python data structures (dic, tuple, list, set) that we use to backend. It works both ways.

class XXArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)  # otomatik olarak oluşur, bu nedenle read_only | occurs automatically so read_only
    writer = serializers.CharField()
    title = serializers.CharField()
    explanation = serializers.CharField()
    text = serializers.CharField()
    city = serializers.CharField()
    publication_date = serializers.DateField()
    status = serializers.BooleanField()

    #? read_only, otomatik olarak auto_now alacağı için | as read_only will get auto_now automatically
    date_of_creation = serializers.DateTimeField(read_only=True)  
    updated_date = serializers.DateTimeField(read_only=True)

#? Frontend'den Backend'e JSON formatlı bilgi geliyorsa POST işlemi ile, bu verilerle bir nesne oluşturmamız gerekir:
#? If JSON formatted information is coming from Frontend to Backend, we need to create an object with this data by POST operation:

    def create(self, validated_data):
        return Article.objects.create(**validated_data)
    
#? Backend'de bulunan bilgileri güncellemek için Frontend'den bir istek alınırsa:
#? If a request is received from the Frontend to update the information available in the Backend:

    def update(self, instance, validated_data):  # instance = eski data | instance = old data

        # Güncellenecek veri olup olmadığını kontrol ediyoruz. | We are checking to see if there is data to be updated.
        instance.writer = validated_data.get("writer", instance)  #? ilgili field = validated data nın içine bak, ilgili field için bir değişiklik var mı diye ? var ise get ile çek , yok ise eski datanın içinden al | Look inside the relevant field = validated data, is there a change for the relevant field? If there is, pull with get, if not, take from old data
        #! Not: bu read_only fields için yapılmaz | #! Note: this is not done for read_only fields
                
        instance.title = validated_data.get("title", instance)         
        instance.explanation = validated_data.get("explanation", instance)         
        instance.text = validated_data.get("text", instance)         
        instance.city = validated_data.get("city", instance)         
        instance.publication_date = validated_data.get("publication_date", instance)         
        instance.status = validated_data.get("status", instance)     
        instance.save()    
        return instance
    
    #? Bu fonksiyonda valided_data'ya müdahale ettik, tüm sınıfı ilgilendiren nesne seviyesinde bir validasyon yaptık.
    #? We intervened validated_data in this function, we made an object level validate that concerns the whole class.
    def validate(self, attrs):
        if attrs['title'] == attrs['explanation']:
            raise serializers.ValidationError('Title and description cannot be the same')
        return attrs
    
    #? Alan bazında tek bir field doğrulama işlemi: validate kelimesinden sonra validayson yapılacak field adını belirtmemiz gerekir.
    #? A single field validation validate operation on a field basis: we have to specify the field name to apply the function name after the word validate.
    def validate_title(self, value):
        if len(value) <= 20:
            raise serializers.ValidationError('The title field must contain at least 20 characters.')
        return value
"""
#! Mevcut bir nesneyi Django Shell plus ile JSON formatına dönüştürelim | Let's convert an existing object to JSON format via django shell plus
>>> from news.models import Article
>>> from news_api.serializers import ArticleSerializer
>>> article_instance = Article.objects.first()
>>> serializer = ArticleSerializer(article_instance)
>>> serializer.data
{'id': 1, 'writer': 'Pakize Kılıç', 'title': 'Backend', 'explanation': 'Backend Mükemmeldir', 'text': 'Backend Django ile mükemmeldir', 'city': 'İSTANBUL', 'publication_date': '2023-03-15', 'status': True, 'date_of_creation': '2023-03-14T17:55:44.495990Z', 'updated_date': '2023-03-14T17:55:44.495990Z'}
>>> from rest_framework.renderers import JSONRenderer
>>> data = JSONRenderer().render(serializer.data)
>>> data
b'{"id":1,"writer":"Pakize K\xc4\xb1l\xc4\xb1\xc3\xa7","title":"Backend","explanation":"Backend M\xc3\xbckemmeldir","text":"Backend Django ile m\xc3\xbckemmeldir","city":"\xc4\xb0STANBUL","publication_date":"2023-03-15","status":true,"date_of_creation":"2023-03-14T17:55:44.495990Z","updated_date":"2023-03-14T17:55:44.495990Z"}'
"""
"""
#! Deserializer yapalım ve yeni bir obje yaratalım | Let's make a deserializer and create a new object
>>> import io
>>> from rest_framework.parsers import JSONParser
>>> stream = io.BytesIO(data)
>>> data = JSONParser().parse(stream)
>>> data
{'id': 1, 'writer': 'Pakize Kılıç', 'title': 'Backend', 'explanation': 'Backend Mükemmeldir', 'text': 'Backend Django ile mükemmeldir', 'city': 'İSTANBUL', 'publication_date': '2023-03-15', 'status': True, 'date_of_creation': '2023-03-14T17:55:44.495990Z', 'updated_date': '2023-03-14T17:55:44.495990Z'}
>>> serializer = ArticleSerializer(data = data)
>>> serializer.is_valid()
True
>>> serializer.validated_data
OrderedDict([('writer', 'Pakize Kılıç'), ('title', 'Backend'), ('explanation', 'Backend Mükemmeldir'), ('text', 'Backend Django ile mükemmeldir'), ('city', 'İSTANBUL'), ('publication_date', datetime.date(2023, 3, 15)), ('status', True)])
>>> serializer.save()
<Article: Backend>
>>> Article.objects.count()
2
>>> exit()
"""


####################### MODEL SERIALIZERS #################################
"""
Modelde olmayan bir field eklemek için:
1- field_name = serializers.SerializerMethodField()

2- def get_field_name(self, obj)

Not: Bu alan veri tabanına kayıt edilmez

To add a field that is not in the model:
1- field_name = serializers.SerializerMethodField()

2- def get_field_name(self, obj)

Note: this field database is not registered
"""

class ArticleSerializer(serializers.ModelSerializer):

    time_since_pub = serializers.SerializerMethodField()
    writer = serializers.StringRelatedField()
    writer_id = serializers.IntegerField()
    class Meta:
        model = Article
        fields = '__all__'  # Bütün fields alır |  Gets all fields
        # exclude = ['id']  # id hariç bütün fields göster | show all fields except id
        

    def get_time_since_pub(self, obj):
        now = datetime.now()
        pub_date = obj.publication_date
        if obj.status == True:
            time_delta = timesince(pub_date, now)
            return time_delta
        
        else:
            return 'Status False'
        
        
    def validate_publication_date(self,date_data ):
        today = date.today()
        if date_data > today:
            raise serializers.ValidationError('publication date forward date cannot be')
        return date_data
    
class JournalistSerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many = True, read_only=True)
    class Meta:
        model = Journalist
        fields = ('id','first_name', 'last_name', 'bio', 'articles')
