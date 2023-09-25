from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from Product.models import Course, Sport
from About.models import AboutUs
from Product.serializer import CourseSerializer
from django.template import loader
from .serializer import *
from django.http import HttpResponse


def home_view(request):
    images = Slider.objects.all().order_by("datetime").values()
    selected = Course.objects.filter(selected=True).order_by("datetime").values()
    course = Course.objects.get(selected=True)
    days = course.days.all()
    about = AboutUs.objects.values().first()
    sport = Sport.objects.all().values()
    template = loader.get_template('public/home.html')
    context = {
        "images": images,
        "selected": selected,
        "days": days,
        "instagram": about["instagram"],
        "telegram": about["telegram"],
        "telephone": about["telephone"],
        "phone": about["phone"],
        "logo": about["logo"],
        "transparent_logo": about["transparent_logo"],
        "address": about["address"],
        "latitude": about["latitude"],
        "longitude": about["longitude"],
        "sport": sport,

    }
    return HttpResponse(template.render(context, request))


@api_view(['GET'])
def get_slider(request):
    images = Slider.objects.all().order_by("datetime")
    ser = SliderSerializer(images, many=True)
    return Response(ser.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_selected(request):
    selected = Course.objects.filter(selected=True).order_by("datetime").first()
    ser = CourseSerializer(selected, many=True)
    return Response(ser.data, status=status.HTTP_200_OK)


class UploadImage(viewsets.ModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        picture = request.data["image"]
        name = request.data["description"]
        Slider.objects.create(description=name, image=picture)
        return Response(status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
def delete_image(request, pk):
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


@api_view(['DELETE'])
def delete_all(request):
    Slider.objects.all().delete()
    return Response("All instances are deleted", status=status.HTTP_204_NO_CONTENT)
