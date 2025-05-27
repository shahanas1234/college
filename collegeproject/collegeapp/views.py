from django.shortcuts import render,redirect
from .models import Course,Teacher,Student
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
import os
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404

# Create your views here.
def course(request):
    return render(request,'course.html')

def addcourse(request):
    if request.method=='POST':
        cname=request.POST['coursename']
        cfees=request.POST['fees']
        course_details=Course(coursename=cname,fees=cfees)
        course_details.save()
        return render(request,'course.html')
    
def signup(request):
     c=Course.objects.all()
     return render(request,'signup.html',{'key':c})

def addteacher(request):
    if request.method=='POST': 
        first_name=request.POST['firstname']
        last_name=request.POST['lastname']
        user_name=request.POST['username']
        age=request.POST['age']
        add=request.POST['address']
        email=request.POST['email']
        phone=request.POST['phone']
        password=request.POST['password']
        cpassword=request.POST['cpass']
        img=request.FILES.get('img')
        course=request.POST['course']
        cs=Course.objects.get(id=course)
        if password==cpassword:
            if User.objects.filter(username=user_name).exists():
                messages.info(request,'This username already exists')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'This email already exists')
                return redirect('signup')
            elif len(phone)!=10:
                messages.info(request,'Phone Number Should Be 10 Digits')
                return redirect('signup')
            else:
                user=User.objects.create_user(first_name=first_name,last_name=last_name,username=user_name,password=password,email=email)
                user.save()
                u=User.objects.get(id=user.id)
                reg=Teacher(age=age,address=add,phone=phone,image=img,course=cs,user=u)
                reg.save()
                return redirect('/')
        else:
            messages.info(request,'Password doesnot match')
            return redirect('signup')
    else:
        messages.info(request,'Registered successfully')
        return render(request,'signup.html')
    
def student(request):
    c=Course.objects.all()
    return render(request,'student.html',{'key':c})

def addstudent(request):
     if request.method=='POST':
        stname=request.POST['name']
        course=request.POST['course']
        cs=Course.objects.get(id=course)
        stage=request.POST['age']
        staddress=request.POST['address']
        dojoin=request.POST['join']
        student_details=Student(studentname=stname,course=cs,age=stage,address=staddress,joiningdate=dojoin)
        student_details.save()
        return redirect('show_student')

def show_student(request):
    st_details=Student.objects.all()
    return render(request,'show_student.html',{'key':st_details})

def edit(request,key):
    st=Student.objects.get(id=key)
    crs=Course.objects.all()
    return render(request,'edit.html',{'key':st,'cou':crs})

def edit_student(request,key):
    if request.method=='POST':
        details=Student.objects.get(id=key)
        details.studentname=request.POST['name']
        c=request.POST['coursename']
        co=Course.objects.get(id=c)
        details.course=co
        details.address=request.POST['address']
        details.age=request.POST['age']
        details.joiningdate=request.POST['join']
        details.save()
        return redirect('show_student')


def delete(request,key):
    st=Student.objects.get(id=key)
    st.delete()
    return redirect('show_student')

def loginpage(request):
    return render(request,'loginpage.html')

# def loginfun(request):
#     if request.method=='POST':
#         username=request.POST['usname']
#         password=request.POST['passd']
#         user=auth.authenticate(username=username,password=password)
#         if user is not None:
#             if user.is_staff:
#                 login(request,user)
#                 return redirect('admin')
#             else:
#                 login(request,user)
#                 auth.login(request,user)
#                 return redirect('login')
#         else:
#             messages.info(request,'Invalid Username or Password')
#             return redirect('login')
#     return render(request,'login.html')

@login_required(login_url='loginpage')
def admin(request):
    return render(request,'admin.html')

def loginfun(request):
    if request.method == 'POST':
        username = request.POST['usname']
        password = request.POST['passd']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_authenticated:  # Check if the user is authenticated
                if user.is_staff:
                    login(request, user)
                    request.session['user'] = user.username  # Set user session variable
                    return redirect('admin')
                else:
                    login(request, user)
                    request.session['user'] = user.username  # Set user session variable
                    messages.info(request, f'Welcome {user}')
                    return redirect('userhome')  # Redirect to techhome after login
            
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('loginpage')
    return render(request, 'signup.html')

@login_required(login_url='loginpage')
def userhome(request):
    if 'user' in request.session:
        return render(request,'userhome.html')

def pageview(request):
    t=Teacher.objects.get(user=request.user)
    return render(request,'pageview.html',{'key':t})

def logout(request):
    auth.logout(request)
    return redirect('loginpage')

def show_teacher(request):
    t=Teacher.objects.all()
    return render(request,'show_teacher.html',{'key':t})

def deleteteacher(request,key):
    st=Teacher.objects.get(id=key)
    u=st.user
    u.delete()
    st.delete()
    return redirect('show_teacher')

def update(request):
    st=Teacher.objects.get(user=request.user)
    crs=Course.objects.all()
    return render(request,'update.html',{'key':st,'cou':crs,'user':request.user})

# def updateuser(request,key):
#     if request.method=='POST':
#         t=Teacher.objects.get(user=key)
#         ph=request.POST['phone']
#         em=request.POST['email']
#         un=request.POST['username']
#         # if User.objects.filter(username=un).exclude(id=key).exists():
#         us=User.objects.exclude(id=key)
#         ex=us.filter(username=un)
#         if ex.exists:
#             messages.error(request,'This username already exists')
#             return redirect('update')
#         if User.objects.filter(email=em).exclude(id=key).exists():
#             messages.error(request,'This email already exists')
#             return redirect('update')
#         elif len(ph)<10:
#             messages.error(request,'Enter 10 digit number')
#             return redirect('update')
        
        
#         else:
#             fn=User.objects.get(id=key)
#             fn.first_name=request.POST['firstname']
#             fn.last_name=request.POST['lastname']
#             fn.user_name=request.POST['username']
#             t.age=request.POST['age']
#             t.address=request.POST['address']
#             fn.email=request.POST['email']
#             t.phone=request.POST['phone']
#             if len(request.FILES)!=0:
#                 if len(t.image)>0:
#                     os.remove(t.image.path)
#                 t.image=request.FILES.get('img')
#             c=request.POST['course']
#             co=Course.objects.get(id=c)
#             t.course=co
#             fn.save()
#             t.save()
#             messages.success(request,'Updated successfully')
#             return redirect('pageview')
#     else:
#         return render(request,'update.html')

def viewcourse(request):
    c=Course.objects.all()
    return render(request,'viewcourse.html',{'key':c})


def editcourse(request,key):
    crs=Course.objects.get(id=key)
    return render(request,'editcourse.html',{'key':crs})

def updatecourse(request,key):
    if request.method=='POST':
        co=Course.objects.get(id=key)
        co.coursename=request.POST['coursename']
        co.fees=request.POST['fees']
        co.save()
        return redirect('viewcourse')


def deletecourse(request,key):
    co=Course.objects.get(id=key)
    co.delete()
    return redirect('viewcourse')
   

# def updateuser(request,t):
#         if request.method == 'POST':
#             u=User.objects.get(id=t)
#             tchr=Teacher.objects.get(user=t)
#             fname=request.POST['firstname']
#             lname=request.POST['lastname']
#             address=request.POST['address']
#             age=request.POST['age']
#             phone=request.POST.get('phone')
#             us=request.POST.get('username')
#             em=request.POST.get('email')
            
            
#             crs=request.POST['course']
#             c=Course.objects.get(id=crs)
#             if User.objects.filter(username=us and t!=u.id).exists():
#                 messages.info(request,'This username already exists')
#                 return redirect('update')
#             elif User.objects.filter(email=em and t!=u.id).exists():
#                 messages.info(request,'This email already exists')
#                 return redirect('update')
#             elif not phone or not phone.isdigit() or len(phone) != 10:
#                 messages.info(request,'Phone Number Should Be 10 Digits')
#                 return redirect('update')
#             else:
#                 if len(request.FILES)!=0:
#                     if len(tchr.image)>0:
#                         os.remove(tchr.image.path)
#                     tchr.image = request.FILES.get('img')
#                 u.first_name=fname
#                 u.last_name=lname
#                 if us:
#                     u.username=us
#                 if em:
#                     u.email=em
#                 u.save()
#                 tchr.age=age
#                 tchr.phone=phone
#                 tchr.address=address
#                 tchr.course=c
#                 tchr.save()
#                 messages.info(request,'Teacher Updated Successfully')
#                 return redirect('pageview')
#         else:
#             return render(request,'update.html')
        



# update teacher

def updateuser(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    user = request.user

    if request.method == 'POST':
        # Get values from POST
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        address = request.POST.get('address')
        course_id = request.POST.get('course')
        image = request.FILES.get('image')
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        if not phone or not phone.isdigit() or len(phone) != 10:
            messages.info(request,'Phone number must be 10 digits.')
            return redirect('update')

       
        elif new_email and new_email != user.email:
            if User.objects.filter(email=new_email).exclude(pk=user.pk).exists():
                messages.info(request,'This email is already in use.')
                return redirect('update')
        elif new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                messages.info(request,'This username is already taken.')
                return redirect('update')
        else:
            teacher.phone = phone
            teacher.age = age
            teacher.address = address
            teacher.course_id = course_id if course_id else None
            if image:
                teacher.image = image
            teacher.save()

            if new_username:
                user.username = new_username
            if new_email:
                user.email = new_email
            user.save()

            messages.success(request,'Profile updated successfully.')
            return redirect('pageview')

  
    return render(request, 'update.html')
        
       
   