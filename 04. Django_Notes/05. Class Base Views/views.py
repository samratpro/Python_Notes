# views.py - Using CBVs with Mixins

from django.shortcuts import get_object_or_404, render
from django.views import View
from .models import Article
from .mixins import LikeAndCommentMixin

class ArticleLikeView(LikeAndCommentMixin, View):
    def get(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        self.like_article(article)
        return render(request, 'article_detail.html', {'article': article})

class ArticleCommentView(LikeAndCommentMixin, View):
    def get(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        self.add_comment_to_article(article, "This is a comment.")
        return render(request, 'article_detail.html', {'article': article})
