from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Course, Lesson, Enrollment, UserLessonCompletion, Profile, User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login as auth_login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, CourseForm, UserUpdateForm, ProfileUpdateForm, DeleteCourseForm
from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST
from django.apps import apps
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView

def home(request):
    # Implement your home view logic here
    return render(request, 'learningPlatform/home.html')

class CourseListView(ListView):
    model = Course
    template_name = 'learningPlatform/course_list.html'
    context_object_name = 'courses'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'learningPlatform/course_detail.html'
    context_object_name = 'course'
    pk_url_kwarg = 'course_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        enrollment = Enrollment.objects.filter(learner=self.request.user, course=course).first()
        is_enrolled = enrollment is not None

        if is_enrolled:
            total_lessons = course.lessons.count()
            completed_lessons = UserLessonCompletion.objects.filter(user=self.request.user, lesson__course=course).count()
            progress = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0
        else:
            progress = 0

        context['is_enrolled'] = is_enrolled
        context['progress'] = progress

        # Add completion status for each lesson
        completed_lesson_ids = UserLessonCompletion.objects.filter(user=self.request.user, lesson__course=course).values_list('lesson_id', flat=True)
        context['completed_lesson_ids'] = completed_lesson_ids

        return context
    


# class LessonDetailView(LoginRequiredMixin, DetailView):
#     model = Lesson
#     template_name = 'learningPlatform/lesson_detail.html'
#     context_object_name = 'lesson'

class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'learningPlatform/lesson_detail.html'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.object.course  # Assuming Lesson model has a 'course' ForeignKey
        return context


# @login_required
# def enroll_course(request, pk):
#     course = get_object_or_404(Course, pk=pk)
#     user = request.user  # Assuming user is authenticated
#     if Enrollment.objects.filter(learner=user, course=course).exists():
#         # User is already enrolled
#         return redirect('course_detail', pk=pk)
#     else:
#         Enrollment.objects.create(learner=user, course=course)
#         return redirect('course_detail', pk=pk)


def enroll_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    Enrollment.objects.get_or_create(learner=user, course=course)
    return redirect('course_detail', course_id=course_id)

def unenroll_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.filter(learner=request.user, course=course).first()
    if enrollment:
        UserLessonCompletion.objects.filter(user=request.user, lesson__course=course).delete()
        enrollment.delete()
    return redirect('course_list')


class LessonListView(LoginRequiredMixin, ListView):
    template_name = 'learningPlatform/lesson_list.html'
    context_object_name = 'lessons'

    def get_queryset(self):
        self.course = get_object_or_404(Course, pk=self.kwargs['course_pk'])
        return Lesson.objects.filter(course=self.course)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        return context


class EnrollmentListView(LoginRequiredMixin, ListView):
    model = Enrollment
    template_name = 'learningPlatform/enrollment_list.html'
    context_object_name = 'enrollments'

    def get_queryset(self):
        return Enrollment.objects.filter(learner=self.request.user)

class EnrollmentDetailView(LoginRequiredMixin, DetailView):
    model = Enrollment
    template_name = 'learningPlatform/enrollment_detail.html'
    context_object_name = 'enrollment'


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'learningPlatform/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'learningPlatform/logout.html', {'user': request.user})

# def custom_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             if user.is_instructor:
#                 return redirect('instructor_dashboard')
#             else:
#                 return redirect('course_list')
#     return render(request, 'learningPlatform/login.html')

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Welcome back, {username}!')

                # Redirect based on user role
                if user.is_instructor:
                    return redirect('instructor_dashboard')
                elif user.is_learner:
                    return redirect('course_list')
                else:
                    return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'learningPlatform/login.html', {'form': form})


@login_required
def course_list(request):
    if request.user.is_learner:
        courses = Course.objects.all()
        enrollments = Enrollment.objects.filter(learner=request.user).values_list('course_id', flat=True)
        return render(request, 'learningPlatform/course_list.html', {'courses': courses, 'enrollments': enrollments})
    else:
        return redirect('home')
    

@login_required
def instructor_dashboard(request):
    if request.user.is_instructor:
        courses = Course.objects.filter(instructor=request.user)
        return render(request, 'learningPlatform/instructor_dashboard.html', {'courses': courses})
    else:
        return redirect('course_list')  # Redirect learners to course list




def course_students(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollments = course.enrollments.all()  # Fetch enrollments related to the course

    context = {
        'course': course,
        'enrollments': enrollments,
    }
    return render(request, 'learningPlatform/course_students.html', context)
# @login_required
# def course_students(request, course_id):
#     course = get_object_or_404(Course, pk=course_id, instructor=request.user)
#     enrollments = Enrollment.objects.filter(course=course)
#     return render(request, 'learningPlatform/course_students.html', {'course': course, 'enrollments': enrollments})


# @login_required
# def add_course(request):
#     if request.method == 'POST':
#         title = request.POST['title']
#         description = request.POST['description']
#         Course.objects.create(title=title, description=description, instructor=request.user)
#         return redirect('instructor_dashboard')
#     return render(request, 'learningPlatform/add_course.html')


@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('instructor_dashboard')
        else:
            print(form.errors)  # Print form errors to the console
            messages.error(request, 'Error creating course. Please check the form and try again.')
    else:
        form = CourseForm()
    return render(request, 'learningPlatform/add_course.html', {'form': form})

# def add_course(request):
#     instructor = request.user  # Assuming user is authenticated
#     if request.method == 'POST':
#         form = CourseForm(request.POST)
#         if form.is_valid():
#             # Process form data
#             form.save()
#             # Redirect or return a success response
#     else:
#         form = CourseForm()

#     context = {
#         'form': form,
#         'instructor': instructor,
#     }
#     return render(request, 'learningPlatform/add_course.html', context)


@login_required
def add_lesson(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        title = request.POST.get('title')
        video_url = request.POST.get('video_url')
        description = request.POST.get('description')

        course = Course.objects.get(pk=course_id)
        Lesson.objects.create(course=course, title=title, video_url=video_url, description=description)
        messages.success(request, 'Lesson added successfully!')
        return redirect('instructor_dashboard')
    
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'learningPlatform/add_lesson.html', {'courses': courses})


# def next_lesson(request, course_id, lesson_id):
#     current_lesson = get_object_or_404(Lesson, id=lesson_id, course_id=course_id)
#     next_lessons = Lesson.objects.filter(course_id=course_id, id__gt=current_lesson.id).order_by('id')
#     if next_lessons.exists():
#         next_lesson = next_lessons.first()
#         return redirect('lesson_detail', pk=course_id, lesson_id=next_lesson.id)
#     else:
#         return redirect('course_detail', pk=course_id)
    
def next_lesson(request, course_pk, lesson_pk):
    course = get_object_or_404(Course, pk=course_pk)
    current_lesson = get_object_or_404(Lesson, pk=lesson_pk, course=course)
    
    # Get the next lesson if it exists
    next_lesson = Lesson.objects.filter(course=course, pk__gt=current_lesson.pk).order_by('pk').first()
    
    if next_lesson:
        # Redirect to the next lesson's detail page
        return redirect('lesson_detail', course_pk=course.pk, lesson_pk=next_lesson.pk)
    else:
        # If no more lessons, display a message or redirect to a course completion page
        return redirect('course_completed') 

@csrf_exempt
def mark_as_completed(request, lesson_id):
    if request.method == 'POST':
        lesson = Lesson.objects.get(pk=lesson_id)
        user = request.user
        UserLessonCompletion.objects.create(user=user, lesson=lesson)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def profile(request):
    if request.method == 'POST':
        form1 = UserUpdateForm(request.POST, instance=request.user)
        form2 = ProfileUpdateForm(request.POST, 
                                  request.FILES, 
                                  instance=request.user.profile)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            messages.success(request, f'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form1 = UserUpdateForm(instance=request.user)
        form2 = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'form1': form1,
        'form2': form2
    }
    return render(request, 'learningPlatform/profile.html', context)


def next_lesson(request, course_pk, pk):
    course = get_object_or_404(Course, pk=course_pk)
    current_lesson = get_object_or_404(Lesson, pk=pk, course=course)
    next_lesson = Lesson.objects.filter(course=course, pk__gt=current_lesson.pk).order_by('pk').first()

    if next_lesson:
        return redirect('lesson_detail', course_pk=course.pk, pk=next_lesson.pk)
    else:
        return redirect('course_completed')


# @login_required
# def mark_completed(request, lesson_id):
#     lesson = get_object_or_404(Lesson, id=lesson_id)
#     request.user.profile.completed_lessons.add(lesson)
#     return redirect('lesson_detail', lesson.pk)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'learningPlatform/change_password.html', {'form': form})


def delete_course(request):
    if request.method == 'POST':
        form = DeleteCourseForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            course_title = course.title
            course.delete()
            messages.success(request, f'The course "{course_title}" was successfully deleted.')
            return redirect('instructor_dashboard')
    else:
        form = DeleteCourseForm()

    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'learningPlatform/delete_course.html', {'form': form, 'courses': courses})


@login_required
def mark_completed(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    profile = request.user.profile
    profile.completed_lessons.add(lesson)
    return JsonResponse({'status': 'completed'})


def course_completed(request):
    return render(request, 'learningPlatform/course_completed.html')


@csrf_exempt
def mark_lesson_completed(request, lesson_id):
    if request.method == 'POST':
        lesson = get_object_or_404(Lesson, id=lesson_id)
        user = request.user

        # Check if the lesson is already marked as completed
        completion, created = UserLessonCompletion.objects.get_or_create(user=user, lesson=lesson)

        return JsonResponse({'status': 'completed'})
    return JsonResponse({'status': 'error'}, status=400)


# @require_POST
# def delete_lesson(request):
#     lesson_id = request.POST.get('lesson_id')
#     lesson = get_object_or_404(Lesson, id=lesson_id)
#     lesson.delete()
#     return JsonResponse({'success': True})

@require_POST
def delete_lesson(request):
    import json
    data = json.loads(request.body)
    lesson_id = data.get('lesson_id')
    try:
        lesson = get_object_or_404(Lesson, id=lesson_id)
        lesson.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_POST
def remove_student(request):
    import json
    data = json.loads(request.body)
    student_id = data.get('student_id')
    try:
        enrollment = get_object_or_404(Enrollment, learner_id=student_id)
        enrollment.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_POST
def message_student(request):
    import json
    data = json.loads(request.body)
    student_id = data.get('student_id')
    message = data.get('message')
    try:
        student = get_object_or_404(User, id=student_id)
        # Logic to send a message to the student
        # For example, you might use an email service or save the message in a database
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    lessons = course.lessons.all()
    completed_lessons = UserLessonCompletion.objects.filter(user=request.user, lesson__in=lessons).count()
    total_lessons = lessons.count()
    progress = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0

    context = {
        'course': course,
        'progress': progress,
        'is_enrolled': request.user in course.students.all(),  # Assuming you have a way to check enrollment
    }

    return render(request, 'learningPlatform/course_detail.html', context)


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'learningPlatform/change_password.html'
