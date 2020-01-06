from ..models import Like
from . import serializers
from rest_framework import generics, status
from rest_framework.response import Response
from posts.api.permissions import IsOwnerOrReadOnly


class LikeListView(generics.ListAPIView):
	queryset = Like.objects.all()
	serializer_class = serializers.LikeSerializer


class LikeCreateView(generics.CreateAPIView):
	queryset = Like.objects.all()

	def get_serializer_class(self):
		post_pk = self.request.data.get("post", 1)
		user = self.request.user
		return serializers.create_like_serializer(post_pk=post_pk, user=user)


class LikeDetailView(generics.RetrieveDestroyAPIView):
	queryset = Like.objects.all()
	serializer_class = serializers.LikeSerializer
	permission_classes = [IsOwnerOrReadOnly]

	def retrieve(self, request, *args, **kwargs):
		super(LikeDetailView, self).retrieve(request, args, kwargs)
		instance = self.get_object()
		serializer = self.get_serializer(instance)
		data = serializer.data
		response = {"status_code": status.HTTP_200_OK,
					"message": "Successfully retrieved",
					"result": data}
		return Response(response)

	def delete(self, request, *args, **kwargs):
		super(LikeDetailView, self).delete(request, args, kwargs)
		response = {"status_code": status.HTTP_200_OK,
					"message": "Successfully deleted"}
		return Response(response)

