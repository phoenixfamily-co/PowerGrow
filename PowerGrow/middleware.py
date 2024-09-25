import re
from django.shortcuts import redirect
import jwt
from django.http import HttpResponse
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from urllib.parse import urlencode, parse_qsl

SECRET_KEY = settings.SECRET_KEY


class SessionAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.non_auth_paths = ['/user/login/', '/user/login/api/', '/home/', '/sport/', '/about/', '/product/',
                               '/reservation/', '/calendar/api/year/', '/user/register/', '/user/register/api/'
                               '/user/register/', '/user/verification/', '/user/verification/api/',
                               '/user/forget/', '/user/forget/api/', '/user/verification/password/',
                               '/user/verification/password/api/', '/']

    def __call__(self, request):
        # بررسی مسیرهای غیر حفاظتی
        for path in self.non_auth_paths:
            if request.path.startswith(path) or re.match(r'^/your-path/[\d]+/$', request.path):
                return self.get_response(request)

        if not request.user.is_authenticated:
            return redirect('user:login')

        return self.get_response(request)


class JWTUrlMiddleware(MiddlewareMixin):
    # کدگذاری URL‌ها به JWT
    def encode_url(self, url):
        try:
            token = jwt.encode({'url': url}, SECRET_KEY, algorithm='HS256')
            return token
        except Exception as e:
            return None

    # رمزگشایی JWT به URL اصلی
    def decode_url(self, token):
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return decoded.get('url')
        except jwt.ExpiredSignatureError:
            return None  # توکن منقضی شده است
        except jwt.InvalidTokenError:
            return None  # توکن نامعتبر است

    def process_request(self, request):
        # رمزگشایی URL قبل از اینکه به View برسد
        token = request.GET.get('encoded_url')
        if token:
            decoded_url = self.decode_url(token)
            if decoded_url:
                # اگر URL رمزگشایی شد، مسیر جدید را درخواستی کنید
                request.path_info = decoded_url
            else:
                return HttpResponse("توکن نامعتبر است یا منقضی شده است", status=400)
        return None

    def process_response(self, request, response):
        # کدگذاری URL‌ها در پاسخ برای خروجی
        if response.status_code == 200:
            full_url = request.get_full_path()  # URL کامل فعلی
            token = self.encode_url(full_url)
            if token:
                # اضافه کردن URL کدگذاری شده به پاسخ
                response['X-Encoded-Url'] = token
        return response
