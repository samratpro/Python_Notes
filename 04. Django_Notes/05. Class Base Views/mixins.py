# mixins.py - Create a mixin

class LikeAndCommentMixin:
    def like_article(self, article):
        article.likes += 1
        article.save()
        return article

    def add_comment_to_article(self, article, comment_text):
        # Handle comments logic here
        return article
