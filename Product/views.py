from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from rest_framework import viewsets
from About.models import AboutUs
from Product.models import Course, Days
from Product.serializer import CourseSerializer, DaysSerializer


def product_view(request, pk, session, day):
    about = AboutUs.objects.values().first()
    product = Course.objects.filter(id=pk).values().first()
    course = Course.objects.get()
    days = course.days.get(id=day, course=pk)
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
        "days": days,
        "type": product["type"],
        "time": product["time"],
        "session": session,
        "tuition": product["tuition"],
        "off": product["off"],
        "price": product["price"],
        "description": product["description"],
        "start": product["start"],
        "image": product["image"],
        "profile":product["profile"],
        "selected": product["selected"],
        "capacity": product["capacity"],
        "gender": product["gender"],
        "datetime": product["datetime"],
    }
    return HttpResponse(template.render(context, request))


def sport_view(request):
    return render(request, "public/product.html")


class CourseView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class DaysView(viewsets.ModelViewSet):
    queryset = Days.objects.all()
    serializer_class = DaysSerializer
