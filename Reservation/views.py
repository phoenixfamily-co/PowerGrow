import datetime
import json

import requests
from arabic_reshaper import arabic_reshaper
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, Http404
from django.template import loader
from django.views.decorators.cache import cache_page
from reportlab.lib.pagesizes import A4
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from About.models import AboutUs
from Product.models import Sport
from Reservation.models import *
from Reservation.serializer import GymSerializer, ReservationSerializer, AdminReservationSerializer
from django.http import FileResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from arabic_reshaper import arabic_reshaper
from bidi.algorithm import get_display
import datetime as dt

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
CallbackURL = 'https://powergrow.net/reservation/verify/'


@cache_page(60 * 15)
def reservation_view(request):
    about = AboutUs.objects.values().first()
    gym = Gym.objects.values().first()
    sport = Sport.objects.all().values()
    year = Year.objects.values().first()
    template = loader.get_template('public/reservation.html')
    context = {
        "about": about,
        "gym": gym,
        "sport": sport,
        "year": year,
    }
    return HttpResponse(template.render(context, request))


def transaction_view(request, gym, time, session, holiday):
    about = AboutUs.objects.values().first()
    gym = Gym.objects.filter(id=gym).values().first()
    times = Time.objects.get(id=time)
    sport = Sport.objects.all().values()
    template = loader.get_template('public/transaction.html')
    context = {
        "about": about,
        "gym": gym,
        "sport": sport,
        "time": times,
        "holiday": holiday,
        "session": session,
    }
    return HttpResponse(template.render(context, request))


def gym_view(request):
    about = AboutUs.objects.values().first()
    gym = Gym.objects.all()
    template = loader.get_template('manager/gym.html')
    context = {
        "about": about,
        "gym": gym,
    }
    return HttpResponse(template.render(context, request))


def admin_gym_view(request):
    about = AboutUs.objects.values().first()
    gym = Gym.objects.all()
    template = loader.get_template('admin/gyms.html')
    context = {
        "about": about,
        "gym": gym,
    }
    return HttpResponse(template.render(context, request))


def reserve_view(request):
    about = AboutUs.objects.values().first()
    reserve = Reservations.objects.filter(success=True).all()
    gym = Gym.objects.all().first()
    user = User.objects.all()
    template = loader.get_template('manager/reserves.html')

    p = Paginator(reserve, 50)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    context = {
        "about": about,
        'page_obj': page_obj,
        "gym": gym,
        "user": user

    }
    return HttpResponse(template.render(context, request))


def admin_reserve_view(request):
    about = AboutUs.objects.values().first()
    reserve = Reservations.objects.filter(success=True).all()
    gym = Gym.objects.all().first()
    template = loader.get_template('admin/reserves.html')
    p = Paginator(reserve, 50)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    context = {
        "about": about,
        'page_obj': page_obj,
        "gym": gym,
    }
    return HttpResponse(template.render(context, request))


def user_reserves_view(request, pk):
    template = loader.get_template('user/reserves.html')
    about = AboutUs.objects.values().first()
    reserves = Reservations.objects.filter(user=pk, success=True).all()

    context = {
        "about": about,
        "reserves": reserves,
    }
    return HttpResponse(template.render(context, request))


@permission_classes([IsAuthenticated])
class GymView(viewsets.ModelViewSet):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer


@permission_classes([IsAuthenticated])
class ReservationView(viewsets.ViewSet):
    queryset = Reservations.objects.all()
    serializer_class = ReservationSerializer

    def list(self, serializer):
        queryset = Reservations.objects.filter(user=self.request.user.id)
        return queryset

    def create(self, serializer):
        data = self.request.data
        authority_data = {
            "MerchantID": settings.MERCHANT,
            "Amount": data["price"],
            "phone": str(self.request.user.number),
            "Description": data["description"],
            "CallbackURL": CallbackURL,
        }
        authority_data = json.dumps(authority_data)
        headers = {'content-type': 'application/json', 'content-length': str(len(authority_data))}
        response = requests.post(ZP_API_REQUEST, data=authority_data, headers=headers, timeout=10)

        try:
            response_data = response.json()  # Parse the response content as JSON
            if response_data['Status'] == 100:
                gym = Gym.objects.filter(id=data["gym"]).first()
                time = Time.objects.filter(id=data["time"]).first()

                Reservations.objects.update_or_create(
                    title=data["title"],
                    description=data["description"],
                    time=time,
                    holiday=data["holiday"],
                    session=data["session"],
                    price=data["price"],
                    gym=gym,
                    user=self.request.user,
                    authority=str(response_data['Authority']),
                    success=False
                )
                return Response({'payment': ZP_API_STARTPAY, 'authority': str(response_data['Authority'])},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Payment request failed'}, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return Response({'error': 'Failed to decode response JSON'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error': 'Missing expected key in response JSON'}, status=status.HTTP_400_BAD_REQUEST)


class ManagerAddReservationView(viewsets.ModelViewSet):
    queryset = Reservations.objects.all()
    serializer_class = AdminReservationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'time'

    def get_queryset(self):
        data = self.kwargs
        queryset = self.queryset.filter(time=data['time'])
        return queryset

    def perform_create(self, serializer):
        data = self.request.data
        session = data["session"]
        gym = Gym.objects.filter(id=data["gym"]).first()
        time = Time.objects.filter(id=self.kwargs['time']).first()
        user = User.objects.filter(number=self.kwargs['user']).first()
        holiday = bool(self.request.POST.get("holiday"))

        if holiday:
            ids = Time.objects.filter(day__name=time.day.name, time=time.time,
                                      day__month__number__gte=time.day.month.number, reserved=False) \
                      .exclude(day__month__number=time.day.month.number,
                               day__number__lt=time.day.number).exclude(
                day__holiday=holiday) \
                      .order_by('day__month__number').values_list('pk', flat=True)[:int(session)]
        else:
            ids = Time.objects.filter(day__name=time.day.name, time=time.time,
                                      day__month__number__gte=time.day.month.number, reserved=False) \
                      .exclude(day__month__number=time.day.month.number,
                               day__number__lt=time.day.number) \
                      .order_by('day__month__number').values_list('pk', flat=True)[:int(session)]

        endDateId = Time.objects.filter(pk__in=list(ids)).order_by("pk").last()
        reservations = Reservations.objects.update_or_create(title=data["title"],
                                                             description=data["description"],
                                                             time=time,
                                                             endDate=endDateId,
                                                             holiday=holiday,
                                                             session=data["session"],
                                                             price=data["price"],
                                                             user=user,
                                                             gym=gym,
                                                             success=True,
                                                             created=self.request.user)

        Time.objects.filter(pk__in=list(ids)).update(reserved=True, res_id=reservations[0].pk)
        serializer = ReservationSerializer(reservations)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        reservation = Reservations.objects.filter(id=self.kwargs['pk']).first()
        if reservation.holiday:
            ids = Time.objects.filter(day__name=reservation.time.day.name, time=reservation.time.time,
                                      day__month__number__gte=reservation.time.day.month.number) \
                      .exclude(day__month__number=reservation.time.day.month.number,
                               day__number__lt=reservation.time.day.number).exclude(day__holiday=reservation.holiday) \
                      .order_by('day__month__number').values_list('pk', flat=True)[:int(reservation.session)]

        else:
            ids = Time.objects.filter(day__name=reservation.time.day.name, time=reservation.time.time,
                                      day__month__number__gte=reservation.time.day.month.number) \
                      .exclude(day__month__number=reservation.time.day.month.number,
                               day__number__lt=reservation.time.day.number) \
                      .order_by('day__month__number').values_list('pk', flat=True)[:int(reservation.session)]

        Time.objects.filter(pk__in=list(ids)).update(reserved=False)
        try:
            reservation.delete()
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(('GET',))
def verify(request):
    reservation = Reservations.objects.get(authority=request.GET.get('Authority', ''))
    about = AboutUs.objects.values().first()
    sport = Sport.objects.all().values()

    context = {
        "about": about,
        "sport": sport,
        "reservation": reservation
    }

    authority_data = {
        "MerchantID": settings.MERCHANT,
        "Authority": reservation.authority,
        "Amount": reservation.price
    }

    data = json.dumps(authority_data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
    response = response.json()
    if response['Status'] == 100:
        template = loader.get_template('public/successful.html')
        reservation.success = True

        if reservation.holiday:
            ids = Time.objects.filter(day__name=reservation.time.day.name, time=reservation.time.time,
                                      day__month__number__gte=reservation.time.day.month.number, reserved=False) \
                      .exclude(day__month__number=reservation.time.day.month.number,
                               day__number__lt=reservation.time.day.number, reserved=False).exclude(
                day__holiday=reservation.holiday) \
                      .order_by('day__month__number').values_list('pk', flat=True)[:int(reservation.session)]
        else:
            ids = Time.objects.filter(day__name=reservation.time.day.name, time=reservation.time.time,
                                      day__month__number__gte=reservation.time.day.month.number) \
                      .exclude(day__month__number=reservation.time.day.month.number,
                               day__number__lt=reservation.time.day.number, reserved=False) \
                      .order_by('day__month__number').values_list('pk', flat=True)[:int(reservation.session)]

        Time.objects.filter(pk__in=list(ids)).update(reserved=True, res_id=reservation.id)

        endDateId = Time.objects.filter(pk__in=list(ids)).order_by("day_id").last()
        endDate = endDateId
        reservation.endDate = endDate
        reservation.save()
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('public/failed.html')
        reservation.time.reserved = False
        reservation.time.save()
        reservation.delete()
        return HttpResponse(template.render(context, request))


def generate_pdf_file(request, pk, end):
    pdfmetrics.registerFont(TTFont('BYekan', 'BYekan.ttf'))
    reservation = Reservations.objects.get(id=pk)
    startDate = f"{reservation.time.day.month.year.number}/{reservation.time.day.month.number}/{reservation.time.day.number}"
    endTime = (dt.datetime.combine(dt.date(1, 1, 1), reservation.time.time) + datetime.timedelta(minutes=90)).time()
    endDateId = Time.objects.get(pk=end)
    endDate = f"{endDateId.day.month.year.number}/{endDateId.day.month.number}/{endDateId.day.number}"

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont('BYekan', 14)
    p.setPageSize(A4)
    p.drawRightString(560, 790, text_converter("تاریخ:"))
    p.drawRightString(200, 790, text_converter("شماره ثبت:"))
    p.drawRightString(320, 760, text_converter("بسمه تعالی"))
    p.drawRightString(342, 730, text_converter("مجموعه ورزشی حجاب"))
    p.drawRightString(355, 700, text_converter("قرارداد اجاره سالن ورزشی"))
    p.drawRightString(560, 670, text_converter("ماده 1 : موضوع قرارداد:"))
    p.drawRightString(560, 650, text_converter("این قرارداد به منظور استفاده از سالن چند منظوره"))
    p.drawRightString(560, 630, text_converter(
        "مجموعه ورزشی حجاب واقع درتهران، بلوار کشاورز، خ حجاب ، روبه روی درب شرقی پارک لاله"))
    p.drawRightString(560, 610, text_converter(
        "بین خانم فاطمه خسروی بابادی به عنوان پیمانکار سالن حجاب به شماره تلفن 09911177140"))
    p.drawRightString(560, 590, text_converter(
        f" و به نمایندگی آقای/خانم {reservation.user.name} به عنوان متقاضی به شماره تلفن {reservation.user.number}"))

    p.drawRightString(560, 570, text_converter("منعقد میشود"))
    p.drawRightString(560, 540, text_converter("ماده 2 : شرایط قرارداد:"))
    p.drawRightString(560, 520,
                      text_converter(f" مدت قرارداد از تاریخ {startDate} لغایت {endDate} به مدت 1 جلسه در هفته"))
    p.drawRightString(560, 500, text_converter(
        f" در روزهای {reservation.time.day.name} از ساعت {reservation.time.time} الی {endTime} که جمعا به میزان {reservation.session} جلسه خواهد بود. "))
    if reservation.holiday:
        p.drawRightString(560, 480, text_converter(
            "روزهای تعطیل محاسبه نشده است."))
    else:
        p.drawRightString(560, 480, text_converter(
            "روزهای تعطیل محاسبه شده است."))

    p.drawRightString(560, 460, text_converter("ماده 3 : مبلغ قرارداد و نحوه پرداخت آن:"))
    p.drawRightString(560, 440, text_converter(
        f" مبلغ قرارداد برای هرجلسه {reservation.time.price}تومان و مبلغ کل قرارداد به میزان{reservation.price}تومان است "))
    p.drawRightString(560, 420, text_converter("که متقاضی آن را در سایت مجموعه به صورت انلاین پرداخت کرده است."))
    p.drawRightString(560, 390, text_converter("ماده 4 : تعهدات طرفین:"))
    p.drawRightString(560, 370, text_converter("۴-۱: میزان ساعت هر جلسه برای استفاده ی متقاضي ۹۰ دقيقه"))
    p.drawRightString(560, 350, text_converter(
        "آموزشی امکان پذیر نیست مگر با مجوز کتبی داده شده توسط مجموعه و حداکثر نفرات استفاده کننده"))
    p.drawRightString(560, 330, text_converter("از سوي متقاضی در هر سانس اعلام باید گردد."))
    p.drawRightString(560, 310, text_converter(
        "۴-۲: متقاضی متعهد مي شود تا نهایت امانت داری را در طي مدت قرارداد رعایت فرماید و مبلغ"))
    p.drawRightString(560, 290, text_converter("هرگونه خسارت به تجهیزات و تاسیسات ورزشی را پرداخت کند."))
    p.drawRightString(560, 270, text_converter(
        "۴-۳: مجموعه ورزشی حجاب میتواند در صورت نیاز به سالن، با اعلام حداقل دو هفته زودتر،"))
    p.drawRightString(560, 250, text_converter(
        "ساعات مورد نیاز خود جابه جا یا قرارداد را به طور کلي لغو کند که در صورت لغو قرارداد، وجوه"))
    p.drawRightString(560, 230, text_converter("واريزي بابت سانس هاي استفاده نشده مسترد خواهدشد."))
    p.drawRightString(560, 210, text_converter(
        "۴-۴ : تعطيلي تمرينات به علت شرایط خاص آن، منوط به نظر مجموعه ورزشی حجاب خواهد بود که"))
    p.drawRightString(560, 190, text_converter(
        "۴-۵: داشتن عضویت در کمیته خدمات درمانی فدراسیون پزشکی ورزشی برای تک تک افراد استفاده"))
    p.drawRightString(560, 170, text_converter(
        "کننده الزامی است؛بنابراین، در صورت هر گونه حادثه برای استفاده کنندگان مسئولیت هزینه ها برعهده ی"))
    p.drawRightString(560, 150, text_converter("متقاضي خواهد بود."))
    p.drawRightString(560, 120, text_converter(
        "ماده ۵: امضا کننده ي قرارداد به عنوان متقاضي، مسئولیت كل مفاد قرارداد را بر عهده می گیرد."))
    p.drawRightString(560, 100, text_converter(
        "ماده ۶: این قرارداد هیچ گونه کسوراتی را در بر نمی گیرد.(شامل هیچ گونه کسوراتی نمی باشد)"))
    p.drawRightString(320, 65, text_converter("صفحه ی 1 از 2"))
    p.showPage()

    p.setFont('BYekan', 14)
    p.setPageSize(A4)

    p.drawRightString(560, 770, text_converter("ماده ۷: فسخ قرارداد:"))
    p.drawRightString(560, 750, text_converter(
        "۷-۱: در صورت مشاهده ی هرگونه تخلف از سوی متقاضی در مفاد این قرارداد، حق فسخ قرارداد به"))
    p.drawRightString(560, 730,
                      text_converter("صورت یک طرفه برای مجموعه ورزشی حجاب محفوظ است و مبلغ واریز شده مسترد نخواهد شد."))
    p.drawRightString(560, 710, text_converter("۷-۲: عدم پرداخت به موقع حق استفاده (ماده ۳ )"))
    p.drawRightString(560, 690, text_converter(
        "لازم به ذکر است پرداخت‌آنلاین در سایت به منزله قبولی و امضا تمامی قوانین و مقررات فوق می باشد"))
    p.drawRightString(560, 660, text_converter(
        "ماده ۸: این قرارداد شامل ۸ ماده و در دو نسخه تنظيم شده است که هر کدام حكم واحد را دارند."))
    p.drawRightString(560, 600, text_converter("مهر و امضا پیمانکار مجموعه حجاب"))
    p.drawRightString(200, 600, text_converter("مهر و امضا متقاضی"))
    p.drawRightString(320, 65, text_converter("صفحه ی 2 از 2"))

    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f"{pk}.pdf")


def text_converter(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text
