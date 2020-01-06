from ..models import Like
from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Post

User = get_user_model()


def create_like_serializer(post_pk=None, user=None):
	class LikeCreateSerializer(serializers.ModelSerializer):
		url = serializers.HyperlinkedIdentityField(
			view_name='detail_like',
			lookup_field='pk'
		)
		user = serializers.SerializerMethodField()
		post = serializers.SerializerMethodField()
		class Meta:
			model = Like
			fields = ('url', 'id', 'user', 'post')

		def get_user(self, obj):
			return str(obj.user.username)

		def get_post(self, obj):
			return str(obj.post.title)

		def validate(self, data):
			post_qs = Post.objects.filter(pk=post_pk)
			if not post_qs.exists():
				raise serializers.ValidationError("Incorrect post id")
			like_qs = Like.objects.filter(post=post_qs.first(), user=user)
			if like_qs.exists():
				raise serializers.ValidationError("Like already exists")
			return data

		def create(self, validated_data):
			post = Post.objects.filter(pk=post_pk).first()
			like = Like(user=user, post=post)
			like.save()
			return like

	return LikeCreateSerializer


class LikeSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(
		view_name='detail_like',
		lookup_field='pk'
	)
	user = serializers.SerializerMethodField()
	post = serializers.SerializerMethodField()

	class Meta:
		model = Like
		fields = ('url', 'id', 'user', 'post')

	def get_user(self, obj):
		return str(obj.user.username)

	def get_post(self, obj):
		return str(obj.post.title)


class LikePostSerializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField()

	class Meta:
		model = Like
		fields = ('id', 'user')

	def get_user(self, obj):
		return str(obj.user.username)


