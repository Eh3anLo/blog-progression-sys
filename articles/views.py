from django.shortcuts import render
from .models import Article
# Create your views here.
def article_detail_view(request , id , slug):
    article = Article.objects.get(pk = id ,slug = slug)
    return render(request , 'articles/article_detail.html' , { 'article' : article})

# def article_detail_view_by_id(request , id , slug):
#     article = Article.objects.get(pk = id , slug=slug)
#     return render(request , 'articles/article_detail.html' , { 'article' : article})