from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from blog_api.paginations import StandardPagination
from blog_app.models import Post, Category, Tag
from blog_api.filters import PostFilter
from blog_api.serializers import PostSerializer, CategorySerializer, UserSerializer, TagSerializer


'''
A viewset that provides default `create()`, `retrieve()`, `update()`, `partial_update()`, `destroy()` and `list()` actions.
'''

####### all Post list which shows all post in one page ################################################################################
'''
@csrf_exempt
def post_list(request):
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)

    elif request.method == "POST":
        # Extract the parameters from the request and serialize them.
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
            
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'POST'])
def post_list_view(request, format=None):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostList(APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = StandardPagination
    authentication_classes = (TokenAuthentication,)

    # use the default filter, designate the filter_fields
    # filterset_fields = ['title']

    # use the self-defined filter
    filterset_class = PostFilter


    # Rewrite the save method (Put API)
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # rewrite the update method (Put API)
    # When updating a ManyToMany field, we need to rewrite the post method. Directly passing the ID will not update it, directly passing the ID will not update it, directly passing the ID will not update it.
    def perform_update(self, serializer):
        post = self.get_object()
        # First, make sure to clear the field. Then, check if any IDs have been uploaded. If IDs have been uploaded, determine whether there are multiple IDs.
        post.tags.clear()
        if self.request.data['tags']:
            # When updating, it is necessary to agree on how to delimit the IDs of the ManyToMany field upon return. For example, we use "," as the delimiter.
            if "," in self.request.data['tags']:
                # We need to extract the value corresponding to tags in request.data, then split the string to retrieve the IDs.
                for id in self.request.data['tags'].split(","):
                    post.tags.add(id)
            else:
                post.tags.add(self.request.data['tags'])
        serializer.save()

    # rewrite the destory method for API delete
    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post is not None:
            post.delete()
            return Response({"message": "delete succeed", "code": "200"}, status=status.HTTP_200_OK)
        return super(PostViewSet, self).destroy(self, request, *args, **kwargs)


# ########### Show detail of one specific detail ############################################################################
'''
@csrf_exempt
def post_detail(request, pk):
    # ?? pk ?????? post ??
    post = get_object_or_404(Post, pk=pk)

    # ?????????? post???????? 404 NOT FOUND
    # ?? settings.py ?? DEBUG ????? True ???django ???? 404 ?????? False ??
    if post is None:
        return HttpResponse(status=404)

    # ?? request ? GET ?????????? pk ? post
    if request.method == 'GET':
        serializer = PostSerializer(post)
        # ??????????? json ??
        return JsonResponse(serializer.data, status=200)

    # ?? request ? PUT ?????? request ?????
    # ??????????????????? 400 BAD REQUEST
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PostSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    # ?? request ? DELETE ????????
    elif request.method == 'DELETE':
        post.delete()
        return HttpResponse(status=204)


@api_view(['GET', 'PUT', 'DELETE'])
def post_detail_view(request, pk, format=None):
    post = get_object_or_404(Post, pk=pk)

    if post is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

'''

class PostDetail(APIView):

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # get the detail of one specific post
    def get(self, request, pk, format=None):
        serializer = PostSerializer(self.get_object(pk=pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        post = self.get_object(pk=pk)
        serializer = PostSerializer(post, data=request.data)

        if serializer.is_valid():
            # When updating a ManyToMany field, we need to rewrite the post method. Directly passing the ID will not update it, directly passing the ID will not update it, directly passing the ID will not update it.
            post.tags.clear()
            if request.data['tags']:
                if "," in request.data['tags']:
                    # We need to extract the value corresponding to tags in request.data, then split the string to retrieve the IDs.
                    for i in request.data['tags'].split(","):
                        post.tags.add(i)
                else:
                    post.tags.add(request.data['tags'])

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        self.get_object(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# ######### show all categories #########################################################
'''
@api_view(['GET', 'POST'])
def categories_view(request, format=None):
    if request.method == 'GET':
        category_list = Category.objects.all()
        serializer = CategorySerializer(category_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_view(request, pk, format=None):
    category = get_object_or_404(Category, pk=pk)

    if category is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response({"code": 200, "message": "delete succeed"}, status=status.HTTP_200_OK)
'''


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # Only the administrator can operate the category
    #permission_classes = (permissions.IsAdminUser,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['name', ]
    pagination_class = StandardPagination

    # rewrite the destory function for delete HTTP method
    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        if category is not None:
            category.delete()
            return Response({"message": "delete succeed"})
        return super(CategoryViewSet, self).destroy(self, request, *args, **kwargs)

####### show all Tags ###############################################
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    #permission_classes = (permissions.IsAdminUser,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['name', ]
    pagination_class = StandardPagination

####### show all User ###########################################
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['username', ]
    pagination_class = StandardPagination

