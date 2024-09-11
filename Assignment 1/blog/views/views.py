from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from .serializers import PostSerializer
from blog.models import Post
import http


# Create your views here.
def hello_view(request):
    return HttpResponse("Hello, Blog!")


def post_list(request: HttpResponse):
    posts = PostSerializer(Post.objects.all(), many=True).data
    return render(request, 'blogs.html', {'posts': posts})
    # match request.method:
    #     case 'GET':
    #         ser = PostSerializer(Post.objects.all(), many=True)
    #         return JsonResponse(ser.data, safe=False)
    #     case 'POST':
    #         ser = PostSerializer(data=request.data, context={'request': request})
    #         if ser.is_valid():
    #             ser.save()
    #             return JsonResponse(ser.data)
    #         return JsonResponse({'error': "error data"}, status=http.HTTPStatus.BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def post_one(request: HttpResponse, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist as e:
        return JsonResponse({'error': str(e)}, status=http.HTTPStatus.BAD_REQUEST)

    match request.method:
        case 'GET':
            return JsonResponse(PostSerializer(post).data)
        case 'PUT':
            ser = PostSerializer(instance=post, data=request.data, context={'request': request})
            if ser.is_valid():
                ser.save()
                return JsonResponse(ser.data)
            return JsonResponse(ser.errors, status=http.HTTPStatus.BAD_REQUEST)
        case 'DELETE':
            post.delete()
            return JsonResponse({'deleted': True})

