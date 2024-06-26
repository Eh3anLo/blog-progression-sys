from django.http import HttpResponseRedirect , HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import PermissionDenied
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView , CreateView , UpdateView , DeleteView , DetailView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from hitcount.views import HitCountDetailView
from .forms import ArticleCreationForm
from .models import Article


# Create your views here.
class ArticleDetailView(HitCountDetailView , DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'id' # select using pk (if not set , select using slug)
    count_hit = True

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        upvotes_connected = get_object_or_404(Article, id=self.kwargs['id'])
        upvoted = False
        if upvotes_connected.upvotes.filter(id=self.request.user.id).exists():
            upvoted = True
        ctx['number_of_upvotes'] = upvotes_connected.number_of_upvotes()
        ctx['article_is_upvoted'] = upvoted
        return ctx

class ArticlesListView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'articles/article_list.html'

    def get_queryset(self):
        return Article.objects.filter(status = 'pub')


class ArticleCreateView(LoginRequiredMixin , CreateView):
    model = Article
    form_class = ArticleCreationForm
    template_name = 'articles/article_create.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save
        return super().form_valid(form)
    

class ArticleUpdateView(UpdateView):
    model = Article
    fields = [
        'title' , 'img' , 'description' , 'status', 'body'
    ]
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('home')
    template_name = 'articles/article_update.html'

    def get_object(self, queryset=None):
        """
        Check the logged in user is the owner of the object or 404
        """
        obj = super(ArticleUpdateView, self).get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionDenied()
        return obj

class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'id'
    context_object_name = 'article'
    template_name = "articles/article_delete.html"

    def get_object(self, queryset=None):
        """
        Check the logged in user is the owner of the object or 404
        """
        obj = super(ArticleDeleteView, self).get_object(queryset)
        if obj.author != self.request.user:
            raise PermissionDenied()
        return obj
    
def article_upvotes_view(request , id , slug):    
    article = get_object_or_404(Article, pk=id )
    if article.upvotes.filter(id=request.user.id).exists():
        article.upvotes.remove(request.user.id)
    else:
        article.upvotes.add(request.user.id)

    # return HttpResponseRedirect(reverse('article_detail', args=[id , slug]))   
    return HttpResponse(article.number_of_upvotes())