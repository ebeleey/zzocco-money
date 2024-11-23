from rest_framework import serializers
from .models import Article, Comment
from django.contrib.auth import get_user_model


User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('username', )


class CommentSerializer(serializers.ModelSerializer):
    class ArticleTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ('title', )

    article = ArticleTitleSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
    
        
class ArticleListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Article
        fields = ('id', 'user', 'title', 'content', 'board_id', 'board_name', 'created_at', )
        

class ArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Article
        fields = ('id', 'user', 'title', 'content', 'board_id', 'board_name', 'created_at', 'updated_at', 'comments', )
        read_only_fields = ('user', )
        


        
        