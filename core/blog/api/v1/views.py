from django.shortcuts import get_object_or_404, get_list_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from blog.models import Post, Category
from .serializers import PostSerializer, CategorySerializer
from .permissions import IsAuthorOrReadOnly


class PostModelViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'author', 'status']
    queryset = Post.objects.all()


class CategoryModelViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()


# Post List & Retrieve View with ViewSet.

'''
class PostViewSet(ViewSet):
    """
    A simple ViewSet for listing or retrieving posts.
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        post_object = get_object_or_404(Post, pk=pk)
        serializer = self.serializer_class(post_object)
        return Response(serializer.data)

    def create(self, request):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
'''

# Post List View in Class Based View with GenericAPIView.

'''
from rest_framework.generics import ListCreateAPIView

class PostListCreateAPIView(ListCreateAPIView):
    """
    getting a list of post and creating new posts.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
'''


# Post List View in Class Based View with APIView.

'''
from rest_framework.views import APIView

class PostListAPIView(APIView):
    """
    getting a list of post and creating new posts.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    def get(self, request):
        """
        retrieving a list of posts.
        :param request:
        :return:
        """
        posts = get_list_or_404(Post)
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        creating a post with provided data.
        :param request:
        :return:
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
'''


# Post List View in Function Based View.

"""
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list_view(request):
    if request.method == 'GET':
        posts = get_list_or_404(Post)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
"""


# Post Detail View in Class Based View with GenericAPIView.

'''
from rest_framework.generics import RetrieveUpdateDestroyAPIView

class PostDetailRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    getting detail of a post, edit and delete the post.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_url_kwarg = 'post_id'
'''


# Post Detail View in Function Based View.

"""
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        post.delete()
        return Response({'detail': 'item removed successfully.'}, status=HTTP_204_NO_CONTENT)
"""


# Post Detail View in Class Based View with APIView.

'''
from rest_framework.views import APIView

class PostDetailCreateAPIView(ListCreateAPIView):
    """
    getting detail of a post, edit and delete the post.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    def get(self, request, post_id):
        """
        retrieving an object of a post class.
        :param request:
        :param post_id:
        :return:
        """
        post = get_object_or_404(Post, pk=post_id)
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    def put(self, request, post_id):
        """
        editing an object of a post class.
        :param request:
        :param post_id:
        :return:
        """

        post = get_object_or_404(Post, pk=post_id)
        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, post_id):
        """
        deleting an object of a post class.
        :param request:
        :param post_id:
        :return:
        """

        post = get_object_or_404(Post, pk=post_id)
        post.delete()
        return Response({'detail': 'item removed successfully.'}, status=HTTP_204_NO_CONTENT)

'''