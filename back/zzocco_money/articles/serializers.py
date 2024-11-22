from rest_framework import serializers
from .models import Article, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_field = ("article", )
        
        
class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'user', 'title', 'content', 'board_id', 'board_name', 'created_at', )
        

class ArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Article
        fields = ('id', 'user', 'title', 'content', 'board_id', 'board_name', 'created_at', 'updated_at', 'comments', )
        read_only_fields = ('user', )
        


        
        