from ..models import Post
from rest_framework import serializers

from likes.api.serializers import LikePostSerializer
from accounts.api.serializers import UserDetailSerializer
from likes.models import Like


class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='detail',
        lookup_field='slug'
    )
    user = UserDetailSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('url', 'id', 'user', 'title', 'content', 'timestamp', 'likes_count', 'likes')


    def get_likes_count(self, obj):
        return obj.like_set.all().count()

    def get_likes(self, obj):
        l_qs = Like.objects.filter(post=obj)
        likes = LikePostSerializer(l_qs, many=True).data
        return likes

