from rest_framework import serializers

from blog.models import Post, Category
from accounts.models import Profile


# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)


class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source='get_snippet')
    absolute_url = serializers.SerializerMethodField(
        method_name='get_absolute_url'
    )
    # category = serializers.SlugRelatedField(
    #     many=False,
    #     slug_field='name',
    #     queryset=Category.objects.all()
    # )

    def get_absolute_url(self, post_obj):
        request = self.context.get('request')
        return request.build_absolute_uri(post_obj.pk)

    def to_representation(self, instance):
        request = self.context.get('request')

        rep = super(PostSerializer, self).to_representation(instance)
        rep['category'] = CategorySerializer(
            instance.category, context={'request': request}
        ).data

        is_retrieve = request.parser_context.get('kwargs').get('pk')
        if is_retrieve is not None:
            rep.pop('snippet', None)
            rep.pop('absolute_url', None)
        else:
            rep.pop('content', None)

        return rep

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author'] = Profile.objects.get(user__id=user_id)
        return super(PostSerializer, self).create(validated_data)

    class Meta:
        model = Post
        fields = (
            'id', 'author', 'title', 'snippet', 'absolute_url', 'content',
            'status', 'category', 'published_date', 'created_date'
        )
        read_only_fields = ('author',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
