# import re
# from django.shortcuts import redirect
# from django.conf import settings
#
#
# SECRET_KEY = settings.SECRET_KEY
#
#
# class SessionAuthMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.non_auth_paths = ['/user/login/', '/user/login/api/', '/home/', '/sport/', '/about/', '/product/',
#                                '/reservation/', '/calendar/api/year/', '/user/register/', '/user/register/api/'
#                                '/user/register/', '/user/verification/', '/user/verification/api/',
#                                '/user/forget/', '/user/forget/api/', '/user/verification/password/',
#                                '/user/verification/password/api/', '/']
#
#     def __call__(self, request):
#         # بررسی مسیرهای غیر حفاظتی
#         for path in self.non_auth_paths:
#             if request.path.startswith(path) or re.match(r'^/your-path/[\d]+/$', request.path):
#                 return self.get_response(request)
#
#         if not request.user.is_authenticated:
#             return redirect('user:login')
#
#         return self.get_response(request)
#
