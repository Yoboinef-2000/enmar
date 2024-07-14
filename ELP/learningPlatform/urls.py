from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from learningPlatform import views as learningPlatform_views

urlpatterns = [
    path('', views.home, name='home'),  # Assuming this is the home page of your platform
    path('courses/', views.course_list, name='course_list'),
    # path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    # path('courses/<int:pk>/enroll/', views.enroll_course, name='enroll_course'),
    # path('courses/<int:course_pk>/unenroll/', views.unenroll_course, name='unenroll_course'),
    path('courses/<int:course_id>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('courses/<int:course_id>/unenroll/', views.unenroll_course, name='unenroll_course'),

    path('courses/<int:course_pk>/lessons/', views.LessonListView.as_view(), name='lesson_list'),
    path('courses/<int:course_pk>/lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('courses/<int:course_pk>/lessons/<int:pk>/next/', views.next_lesson, name='next_lesson'),
    path('enrollments/', views.EnrollmentListView.as_view(), name='enrollment_list'),
    path('enrollments/<int:pk>/', views.EnrollmentDetailView.as_view(), name='enrollment_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', learningPlatform_views.profile, name='profile'),
    path('instructor/dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('instructor/course/<int:course_id>/students/', views.course_students, name='course_students'),
    path('instructor/add_course/', views.add_course, name='add_course'),
    path('add_lesson/', views.add_lesson, name='add_lesson'),
    path('mark_as_completed/<int:lesson_id>/', views.mark_as_completed, name='mark_as_completed'),
    path('lesson/<int:lesson_id>/complete/', views.mark_completed, name='mark_completed'),
    # path('change_password/', views.change_password, name='change_password'),
    path('delete_course/', views.delete_course, name='delete_course'),
    path('course_completed/', views.course_completed, name='course_completed'),
    path('delete-lesson/', views.delete_lesson, name='delete_lesson'),
    path('remove-student/', views.remove_student, name='remove_student'),
    path('message-student/', views.message_student, name='message_student'),
    path('change_password/', views.CustomPasswordChangeView.as_view(), name='change_password'),

]


# from django.urls import path, include
# from . import views
# from django.contrib.auth import views as auth_views
# from learningPlatform import views as learningPlatform_views

# urlpatterns = [
#     path('', views.home, name='home'),  # Assuming this is the home page of your platform
#     # path('courses/', views.CourseListView.as_view(), name='course_list'),
#     path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
#     path('courses/<int:pk>/enroll/', views.enroll_course, name='enroll_course'),
#     path('courses/<int:course_pk>/lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
#     path('courses/<int:course_pk>/lessons/', views.LessonListView.as_view(), name='lesson_list'),
#     path('enrollments/', views.EnrollmentListView.as_view(), name='enrollment_list'),
#     path('enrollments/<int:pk>/', views.EnrollmentDetailView.as_view(), name='enrollment_detail'),
#     # path('accounts/', include('django.contrib.auth.urls')),
#     # path('login/', auth_views.LoginView.as_view(template_name='learningPlatform/login.html'), name='login'),
#     path('register/', views.register, name='register'),
#     path("logout/", views.logout_view, name="logout"),
#     path('courses/', views.course_list, name='course_list'),
#     path('login/', views.custom_login, name='login'),
#     path('profile/', learningPlatform_views.profile, name='profile'),
#     path('instructor/dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
#     path('instructor/course/<int:course_id>/students/', views.course_students, name='course_students'),
#     path('instructor/add_course/', views.add_course, name='add_course'),
#     path('add_lesson/', views.add_lesson, name='add_lesson'),
#     path('courses/<int:course_id>/lessons/<int:lesson_id>/next/', views.next_lesson, name='next_lesson'),
#     path('mark_as_completed/<int:lesson_id>/', views.mark_as_completed, name='mark_as_completed'),
#     path('lesson/<int:lesson_id>/complete/', views.mark_completed, name='mark_completed'),
#     path('change_password/', views.change_password, name='change_password'),
#     path('delete_course/', views.delete_course, name='delete_course'),
#     path('course_completed/', views.course_completed, name='course_completed'),
#     path('courses/<int:course_pk>/lessons/<int:lesson_pk>/next/', views.next_lesson, name='next_lesson'),


# ]




