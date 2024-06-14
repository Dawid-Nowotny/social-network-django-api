from rest_framework import serializers

from .models import Post, PostImage

class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = PostImage
        fields = ['image']

class PostSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True
    )

    class Meta:
        model = Post
        fields = ['content', 'images']

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        post = Post.objects.create(author=self.context['request'].user, **validated_data)
        for image_data in images_data:
            PostImage.objects.create(post=post, image=image_data)
        return post

class PostDetailSerializer(PostSerializer):
    author = serializers.StringRelatedField()
    creation_date = serializers.DateField()
    likes = serializers.StringRelatedField(many=True, read_only=True)

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['author', 'creation_date', 'likes']