from django.db import models

# Create your models here.

class Journalist(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=150)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f" {self.first_name} {self.last_name} "
class Article(models.Model):
    writer = models.ForeignKey(Journalist, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=100)
    explanation = models.CharField(max_length=200)
    text = models.TextField()
    city = models.CharField(max_length=50)
    publication_date = models.DateField()
    status = models.BooleanField(default=True)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

