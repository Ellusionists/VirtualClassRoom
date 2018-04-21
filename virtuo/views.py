# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.conf import settings
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import View, DetailView, CreateView, UpdateView, ListView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserForm, StudentForm, TeacherForm, MaterialModelForm, EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import Material, Student, Teacher, Question, Course



# Create your views here.

def first_view(request):
    logged_in_as = None
    course_details = None  
    courses = []
    if not request.user.is_authenticated:
        return render(request, 'text.html', {'name':'Not authenticated','logout_button':False,'logged_in_as':logged_in_as})
    if Student.objects.filter(user=request.user):
        logged_in_as = "Student"
        course_details = Student.objects.filter(user=request.user).values('courses')
        for i in course_details:
            print(i.values())
            temp = Course.objects.filter(course_id=i.values()[0]).values()
            print(temp)
            courses.append(Course.objects.filter(course_id=i.values()[0]).values())
        print(courses)
        print(course_details)
    elif Teacher.objects.filter(user=request.user):
        logged_in_as = "Teacher"
        course_details = Teacher.objects.filter(user=request.user).values('courses')
        for i in course_details:
            print(i.values())
            temp = Course.objects.filter(course_id=i.values()[0]).values()
            print(temp)
            courses.append(Course.objects.filter(course_id=i.values()[0]).values())
        print(courses)
        print(course_details)
    return render(request, 'text.html', {'name':request.user.username,'logout_button':True,'logged_in_as':logged_in_as, 'course_details':course_details, 'courses':courses})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        print(username)
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('first_view')
        return render(request, 'login.html', {})
    return render(request, 'login.html', {})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    return redirect('login')

class UserRegister(View):
    form_class = UserForm
    template_name = 'register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # email = form.cleaned_data['email']
            user.is_active = True
            user.set_password(password)
            print(password+"vjh")
            user.save()
            message = "registered successfully"
            login(request, user)
            return redirect('first_view')
        return render(request, self.template_name, {'form':form})

# class DetailView(DetailView):
#     model = User
#     template_name = 'detail.html'

class StudentRegister(View):
    form_class = StudentForm
    template_name = 'studentregister.html'

    def get(self, request):
        if request.user.is_authenticated:
            form = self.form_class(None)
            return render(request, self.template_name, {'form':form})
        return redirect('register')

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            enrollment_no = form.cleaned_data['enrollment_no'] 
            courses = form.cleaned_data['courses']
            for i in courses:
                student.courses.add(i)
            print(enrollment_no)
            print(courses)
            student.save()
            return redirect('first_view')
        return render(request, self.template_name, {'form':form})

class TeacherRegister(View):
    form_class = TeacherForm
    template_name = 'teacherregister.html'

    def get(self, request):
        if request.user.is_authenticated:
            form = self.form_class(None)
            return render(request, self.template_name, {'form':form})
        return redirect('register')
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.user = request.user
            courses = form.cleaned_data['courses']
            for i in courses:
                teacher.courses.add(i)
            teacher.save()
            return redirect('first_view')
        return render(request, self.template_name, {'form':form})

class MaterialCreateView(View):
    model = Material
    template_name = "addCourse.html"
    form_class = MaterialModelForm

    # success_url = "/view/"
    # uploaded_by = request.user.username;

    # @method_decorator(login_required)
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})

    def post(self, request):    
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.uploaded_by = request.user.username
            material.save()
            return redirect('first_view')
        return render(request, self.template_name, {'form':form})

class MaterialDetailView(DetailView):
    model = Material

class MaterialDeleteView(DeleteView):
    model = Material
    success_url = "/"

class MaterialListView(ListView):
    model = Material

class CourseListView(ListView):
    model = Course

class CourseDetailView(DetailView):
    model = Course

    def get_context_data(self, **kwargs):
        object = kwargs['object']
        taught_by = []
        users = User.objects.all()
        for item in users:
            if Teacher.objects.filter(user=item):
                course_details = Teacher.objects.filter(user=item).values('courses')
                for course in course_details:
                    print(course['courses'])
                    if object.course_id == course['courses']: 
                        # print(item.username) 
                        taught_by.append(item.username)
        context = {'object':object,'name':'lulz','taught_by':taught_by}
        return context



class MaterialDownloadView(DetailView):
    model = Material

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        filepath = os.path.join(settings.MEDIA_ROOT, str(obj.material_link))
        print(filepath)
        wrapper = FileWrapper(file(filepath))
        response = HttpResponse(wrapper, content_type = "application/force-download")
        response["Content-Disposition"] = "attachment; filename = %s" %(obj.material_name)
        response["X-SendFile"] = str(obj.material_name)
        return response

    # def get_queryset(self):
    #     return Material.objects.filter(Course__course_id = Student__)

def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'profile.html', args)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(('/profile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
    return render(request, 'profile_edit.html', args)

# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(data=request.POST, user=request.user)

#         if form.is_valid():
#             form.save()
#             update_session_auth_hash(request, form.user)
#             return redirect(reverse('profile'))
#         else:
#             return redirect(reverse('change_password'))
#     else:
#         form = PasswordChangeForm(user=request.user)

#         args = {'form': form}
#     return render(request, 'change_password.html', args)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('edit_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })