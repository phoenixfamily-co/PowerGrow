from django.shortcuts import render
from rest_framework import viewsets
from Product.models import Course
from Product.serializer import CourseSerializer
from rest_framework.response import Response
from rest_framework import status


def product_view(request):
    return render(request, "product.html")


def sport_view(request):
    return render(request, "product.html")


class Create_Course(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def create(self, request, *args, **kwargs):
        title = request.data["title"]
        name = request.data["description"]
        day = request.data["day"]
        type = request.data["type"]
        time = request.data["time"]
        session = request.data["session"]
        tuition = request.data["tuition"]
        price = request.data["price"]
        description = request.data["description"]
        image = request.data["image"]
        selected = bool(request.POST.get("selected", False))
        capacity = request.data["capacity"]
        gender = request.data["gender"]
        Course.objects.create(title=title, name=name, day=day, type=type, time=time, session=session, tuition=tuition,
                              price=price, description=description, image=image, selected=selected, capacity=capacity,
                              gender=gender)
        return Response(status=status.HTTP_201_CREATED)
