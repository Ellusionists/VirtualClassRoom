from django.contrib.auth.models import User

from django import forms
from .models import Course, Student, Teacher, Material, Question

class UserForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

class StudentForm(forms.ModelForm):
    courses = forms.ModelMultipleChoiceField(queryset=Course.objects.all())
    class Meta:
        model = Student
        fields = ['enrollment_no', 'courses']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher_id', 'courses']

class MaterialModelForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = [
            "material_name",
            "material_link",
            "related_course",
            "m_type",
            ]


