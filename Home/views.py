from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser , MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from .serializer import *
from django.shortcuts import render


def home_view(request):
    return render(request, "home.html")


@api_view(['GET'])
def get_slider(request):
    images = Slider.objects.all()
    ser = SliderSerializer(images, many=True)
    return Response(ser.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_article(request):
    articles = Article.objects.all()
    ser = ArticleSerializer(articles, many=True)
    return Response(ser.data, status=status.HTTP_200_OK)


class UploadImage(viewsets.ModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def post_article(request):
    ser = ArticleSerializer(data=request.data)
    if ser.is_valid():
        ser.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def get_update_delete_image(request, pk):
    try:
        image = Slider.objects.get(pk=pk)

    except(Exception,):
        return Response({"error": "Not Found!"}, status=status.HTTP_404_NOT_FOUND)
    else:
        if request.method == "PUT":
            ser = SliderSerializer(image, data=request.data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=status.HTTP_200_OK)
            else:
                return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'GET':
            ser = SliderSerializer(image)
            return Response(ser.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            image.delete()
            return Response("article deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def get_update_delete_article(request, pk):
    try:
        article = Article.objects.get(pk=pk)

    except(Exception,):
        return Response({"error": "Not Found!"}, status=status.HTTP_404_NOT_FOUND)
    else:
        if request.method == "PUT":
            ser = ArticleSerializer(article, data=request.data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=status.HTTP_200_OK)
            else:
                return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'GET':
            ser = ArticleSerializer(article)
            return Response(ser.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            article.delete()
            return Response("article deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def delete_all(request):
    Slider.objects.all().delete()
    return Response("All instances are deleted", status=status.HTTP_204_NO_CONTENT)
