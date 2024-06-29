from django.contrib.auth.models import User
from rest_framework import serializers

from blog_app.models import Post, Category, Tag


# class PostSerializer(serializers.Serializer):
#     # The list of fields that need to be serialized and deserialized.
#     # allow_blank, allow_null, default, error_messages, format, help_text, initial, input_formats, label, max_length,
#     # min_length, required, read_only, style, source, trim_whitespace, validators, write_only,
#     title = serializers.CharField(max_length=70)
#     body = serializers.CharField()
#     create_time = serializers.DateTimeField()
#     modified_time = serializers.DateTimeField()
#     excerpt = serializers.CharField(max_length=200, allow_blank=True)
#
#     # define the create method
#     def create(self, validated_data):
#         return Post.objects.all(**validated_data)
#
#     # define the update method
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.body = validated_data.get('body', instance.body)
#         instance.create_time = validated_data.get('create_time', instance.create_time)
#         instance.modified_time = validated_data.get('modified_time', instance.modified_time)
#         instance.excerpt = validated_data.get('excerpt', instance.excerpt)


class TagSerializer(serializers.ModelSerializer):
    # The list of fields that need to be serialized and deserialized.
    class Meta:
        model = Tag
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    # author = UserSerializer()
    author = serializers.ReadOnlyField(source='author.username')
    author_id = serializers.ReadOnlyField(source='author.id')
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    # posts = serializers.StringRelatedField(many=True)
    # posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
        #exclude = ['password', 'last_login', 'groups' ]
