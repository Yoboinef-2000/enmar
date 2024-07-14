from django import forms
from .models import User, Course, Enrollment
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Profile



class CustomPasswordInput(forms.PasswordInput):
    def render(self, name, value, attrs=None, renderer=None):
        return super().render(name, value, attrs=attrs, renderer=renderer).replace('type="password"', 'type="text"')

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_learner', 'is_instructor', 'bio']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        # fields = ['title', 'description', 'category', 'instructor', 'target_audience', 'estimated_time', 'thumbnail']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instructor'].queryset = User.objects.filter(is_instructor=True)
        

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['learner'].queryset = User.objects.filter(is_learner=True)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']
        

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class DeleteCourseForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label="Select a Course", required=True)

        