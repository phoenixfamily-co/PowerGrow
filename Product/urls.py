from django.urls import path
from Product.views import *

app_name = 'product'

urlpatterns = [
    path('api/sport/create/', SportView.as_view({'post': 'create'}), name='create_sports'),
    path('api/sport/delete/<int:pk>/', SportView.as_view({'delete': 'destroy'}), name='delete-sports'),
    path('api/sport/update/<int:pk>/', SportView.as_view({'put': 'update'}), name='update-sports'),
    path('api/sport/', SportView.as_view({'get': 'list'}), name='sports'),
    path('sport/<int:pk>/', category_view, name='category'),
    path('sports/', sports_view, name='sports_view'),
    path('sports/admin/', admin_sports_view, name='sports_view_admin'),
    path('api/course/create/', CourseView.as_view({'post': 'create'}), name='create_courses'),
    path('api/course/delete/<int:pk>/', CourseView.as_view({'delete': 'destroy'}), name='delete-courses'),
    path('api/course/update/<int:pk>/', UpdateCourse.as_view(), name='update-courses'),
    path('api/course/title/update/<int:pk>/', ChangeCourseTitle.as_view(), name='update-courses-title'),
    path('api/course/name/update/<int:pk>/', ChangeCourseName.as_view(), name='update-courses-name'),
    path('api/course/gender/update/<int:pk>/', ChangeCourseGender.as_view(), name='update-courses-gender'),
    path('api/course/type/update/<int:pk>/', ChangeCourseType.as_view(), name='update-courses-type'),
    path('api/course/time/update/<int:pk>/', ChangeCourseTime.as_view(), name='update-courses-time'),
    path('api/course/capacity/update/<int:pk>/', ChangeCourseCapacity.as_view(), name='update-courses-capacity'),
    path('api/course/sport/update/<int:pk>/', ChangeCourseSport.as_view(), name='update-courses_sport'),
    path('api/course/', CourseView.as_view({'get': 'list'}), name='courses'),
    path('course/', courses_view, name='courses_view'),
    path('course/admin/', admin_courses_view, name='courses_view_admin'),
    path('course/user/<int:pk>/', user_courses_view, name='courses_view_user'),
    path('course/teacher/<int:pk>/', teacher_courses_view, name='courses_view_teacher'),
    path('api/sessions/create/', SessionView.as_view({'post': 'create'}), name='creat_sessions'),
    path('api/sessions/delete/<int:pk>/', SessionView.as_view({'delete': 'destroy'}), name='delete_sessions'),
    path('api/sessions/update/<int:pk>/', SessionView.as_view({'put': 'update'}), name='update_sessions'),
    path('api/sessions/<int:pk>/', SessionView.as_view({'get': 'list'}), name='sessions'),
    path('sessions/', session_view, name='sessions_view'),
    path('sessions/admin/', admin_session_view, name='sessions_view_admin'),
    path('api/days/create/', DaysView.as_view({'post': 'create'}), name='create_days'),
    path('api/days/delete/<int:pk>/', DaysView.as_view({'delete': 'destroy'}), name='delete-days'),
    path('api/days/update/<int:pk>/', DaysView.as_view({'put': 'update'}), name='update-days'),
    path('api/days/<int:pk>/', DaysView.as_view({'get': 'list'}), name='days'),
    path('days/', day_view, name='days-view'),
    path('days/admin/', admin_day_view, name='days-view_admin'),
    path('api/participate/', ParticipationView.as_view({'post': 'create'}), name='participate'),
    path('api/admin/participate/<int:pk>/delete/', ManagerParticipationView.as_view({'delete': 'destroy'}),
         name='delete-admin-participate'),
    path('api/admin/register/<int:id>/<int:session>/<int:day>/<int:start>/create/', RegisterParticipants.as_view
    ({'post': 'create'}),
         name='create-admin-participate'),
    path('api/admin/participate/<int:id>/<int:session>/<int:day>/<int:start>/<int:user>/create/', ManagerParticipationView.as_view
    ({'post': 'create'}),
         name='create-admin-participate'),
    path('api/admin/participate/<int:id>/<int:session>/<int:day>/<int:start>/update/',
         ManagerParticipationView.as_view({'put': 'update'}),
         name='update-admin-participate'),

    path('api/admin/participate/<int:id>/delete/',
         ManagerParticipationView.as_view({'delete': 'destroy'}),
         name='delete-admin-participate'),

    path('api/admin/participate/', ManagerParticipationView.as_view({'get': 'list'}),
         name='admin-participate'),

    path('api/end/<int:pk>/', ChangeDayView.as_view(), name='change_end'),

    path('api/description/<int:pk>/', ChangeDescriptionView.as_view(), name='change_description'),

    path('api/search/<int:pk>/', SearchView.as_view(), name='search'),
    path('payment/<int:pk>/<int:session>/<int:day>/<int:start>/', payment_view, name='payment'),
    path('check/<int:pk>/<int:session>/<int:day>/', check_view, name='check'),
    path('api/participants/<int:pk>/', CourseUserView.as_view(), name='course_user'),
    path('<int:pk>/', product_view, name='product'),
    path('verify/', verify, name='verify'),
    path('list/teacher/<int:pk>/', teacher_user_list, name='teacher_user_list'),
    path('list/manager/<int:pk>/', manager_user_list, name='manager_user_list'),

]
