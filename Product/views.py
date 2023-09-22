from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from rest_framework import viewsets
from About.models import AboutUs
from Product.models import Course
from Product.serializer import CourseSerializer
from rest_framework.response import Response
from rest_framework import status


def product_view(request, pk):
    about = AboutUs.objects.values().first()
    product = Course.objects.filter(id=pk).values().first()
    template = loader.get_template('public/product.html')
    context = {
        "instagram": about["instagram"],
        "telegram": about["telegram"],
        "telephone": about["telephone"],
        "phone": about["phone"],
        "logo": about["logo"],
        "transparent_logo": about["transparent_logo"],
        "address": about["address"],
        "latitude": about["latitude"],
        "longitude": about["longitude"],
        "title": product["title"],
        "name": product["name"],
        "day": product["day"],
        "type": product["type"],
        "time": product["time"],
        "session": product["session"],
        "tuition": product["tuition"],
        "off": product["off"],
        "price": product["price"],
        "description": product["description"],
        "start": product["start"],
        "image": product["image"],
        "selected": product["selected"],
        "capacity": product["capacity"],
        "gender": product["gender"],
        "datetime": product["datetime"],
    }
    return HttpResponse(template.render(context, request))


def sport_view(request):
    return render(request, "public/product.html")


class Create_Course(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def create(self, request, *args, **kwargs):
        title = request.data["title"]
        name = request.data["name"]
        day = request.data["day"]
        type = request.data["type"]
        time = request.data["time"]
        session = request.data["session"]
        tuition = request.data["tuition"]
        off = request.data["off"]
        price = (int(tuition) - int(off) * int(tuition) / 100)
        description = request.data["description"]
        image = request.data["image"]
        selected = bool(request.POST.get("selected", False))
        capacity = request.data["capacity"]
        gender = request.data["gender"]
        Course.objects.create(title=title, name=name, day=day, type=type, time=time, session=session, tuition=tuition,
                              price=price, description=description, image=image, selected=selected, capacity=capacity,
                              gender=gender)
        return Response(status=status.HTTP_201_CREATED)
