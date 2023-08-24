from django.shortcuts import render


def reservation_view(request):
    return render(request, "reservation.html")
