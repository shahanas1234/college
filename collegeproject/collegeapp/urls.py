from django.urls import path
from .import views

urlpatterns = [
   path('course',views.course,name='course'),
   path('addcourse',views.addcourse,name='addcourse'),
   path('signup',views.signup,name='signup'),
   path('addteacher',views.addteacher,name='addteacher'),
   path('student',views.student,name='student'),
   path('addstudent',views.addstudent,name='addstudent'),
   path('show_student',views.show_student,name='show_student'),
   path('edit/<int:key>',views.edit,name='edit'),
   path('delete/<int:key>',views.delete,name='delete'),
   path('edit_student/<int:key>',views.edit_student,name='edit_student'),
   path('',views.loginpage,name='loginpage'),
   path('loginfun',views.loginfun,name='loginfun'),
   path('admin',views.admin,name='admin'),
   path('userhome',views.userhome,name='userhome'),
   path('pageview',views.pageview,name='pageview'),
   path('logout',views.logout,name='logout'),
   path('show_teacher',views.show_teacher,name='show_teacher'),
   path('deleteteacher/<int:key>',views.deleteteacher,name='deleteteacher'),
   path('update',views.update,name='update'),
   path('updateuser',views.updateuser,name='updateuser'),
   path('viewcourse',views.viewcourse,name='viewcourse'),
   path('editcourse/<int:key>',views.editcourse,name='editcourse'),
   path('updatecourse/<int:key>',views.updatecourse,name='updatecourse'),
    path('deletecourse/<int:key>',views.deletecourse,name='deletecourse')

]