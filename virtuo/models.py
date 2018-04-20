# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Course(models.Model):
    course_name = models.CharField(max_length = 35, null = False, blank = False)
    course_id = models.CharField(max_length = 35, null = False, blank = False, unique = True, primary_key = True)
    credits = models.IntegerField(null = False, blank = False)

    # def __str__(self):
    #     return "%s %s %s" % (self.course_name, self.course_id, self.credits)

    def __str__(self):
        return "%s" % (self.course_id)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, default = 1)
    enrollment_no = models.CharField(max_length = 35, primary_key = True ,unique = True, null = False, blank = False)
    courses = models.ManyToManyField(Course, default= 'None selected')

    def __str__(self):
        return self.enrollment_no

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, default = 1)
    teacher_id = models.CharField(max_length = 35, primary_key = True ,unique = True, null = False, blank = False)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.teacher_id

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.uploaded_by, filename)


class Material(models.Model):
    M_TYPE = (
        ('PPT', 'Presentation'),
        ('VID', 'Video'),
    )


    material_name = models.CharField(max_length = 35, null = False, blank = False)
    material_link = models.FileField(upload_to = user_directory_path, null = True, blank = True)
    uploaded_by = models.CharField(max_length = 35, null = True, blank = True)
    related_course = models.ForeignKey(Course, on_delete = models.CASCADE, null = False)
    m_type = models.CharField(max_length = 3, choices = M_TYPE, null = True)

    def __str__(self):
        return "%s" % (self.material_name)

    def get_course(self):
        return "%s" % (self.related_course)
 
    def get_material_id(self):
        return "%d" % (self.id)

    def get_download_path(self):
        return "%s/%s" % (DIR, self.material_link)

    # def __str__(self):
    #     return "%s %s" % (self.material_name, self.uploaded_by)

class Question(models.Model):
    question_id = models.CharField(max_length = 35, null = False, blank = False, primary_key = True) #Add verbose name
    material_id = models.ForeignKey(Material, on_delete = models.CASCADE)
    question = models.TextField(null = True, blank = True)
    asked_by = models.CharField(max_length = 10)
    answered_by = models.CharField(max_length = 10)
    date_time = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return "%s %s" % (self.question_id, self.material_id)