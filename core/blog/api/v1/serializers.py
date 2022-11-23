from rest_framework import serializers

from blog.models import Post, Category


# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)


class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source='get_snippet')
    absolute_url = serializers.SerializerMethodField(method_name='get_absolute_url')

    def get_absolute_url(self, post_obj):
        request = self.context.get('request')
        return request.build_absolute_uri(post_obj.pk)

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'title',
            'snippet',
            'absolute_url',
            'content',
            'status',
            'category',
            'published_date',
            'created_date'
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
