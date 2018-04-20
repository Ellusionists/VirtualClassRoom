from django.conf.urls import url
from django.conf.urls import include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.first_view, name= 'first_view'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'logout/$', views.logout_view, name='logout'),
    url(r'^register/', views.UserRegister.as_view(), name = 'register'),
    url(r'studentregister/', views.StudentRegister.as_view(), name = 'studentregister'),
    url(r'teacherregister/', views.TeacherRegister.as_view(), name = 'teacherregister'),
    # url(r'^student/(?P<pk>[0-9]+)/$', views.StudentDetailView.as_view(), name = 'studentdetail'),
    url(r'^create/$', views.MaterialCreateView.as_view(), name='create'),
	url(r'^view/(?P<pk>\d+)/$', views.MaterialDetailView.as_view(), name='detail'),
    url(r'^delete/(?P<pk>\d+)/$', views.MaterialDeleteView.as_view(), name='delete'),
    url(r'^view/$', views.MaterialListView.as_view(), name='material-list'),
   	url(r'^view/(?P<pk>\d+)/download$', views.MaterialDownloadView.as_view(), name='download'),
    url(r'^course-list/$', views.CourseListView.as_view(), name='course-list'),
	url(r'^course/(?P<pk>[\w-]+)/$', views.CourseDetailView.as_view(), name='course-detail'),
]