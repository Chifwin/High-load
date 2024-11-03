from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from main.models import KeyValue
from main.serializers import KeyValueSerializer
from django.http import Http404


# Create your views here.

class KeyValueAddView(APIView):
    def post(self, request):
        serializer = KeyValueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KeyValueView(APIView):
    def get_object(self, key):
        try:
            return KeyValue.objects.get(key=key)
        except KeyValue.DoesNotExist:
            raise Http404

    def get(self, request, key):
        kv = self.get_object(key)
        serializer = KeyValueSerializer(kv)
        return Response(serializer.data)

    def put(self, request, key):
        kv = self.get_object(key)
        serializer = KeyValueSerializer(kv, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, key):
        kv = self.get_object(key)
        kv.delete()
        return Response(status=status.HTTP_200_OK)
