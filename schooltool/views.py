from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User


from .models import Course
# Create your views here.

def index(request):
  return render(request, 'schooltool/index.html')

def login(request):
    context = {"Error": False}
    if request.method == "GET":
        return render(request, 'schooltool/login.html')
    if request.method == "POST":
        username = request.post["username"]
        password = request.post["password"]
        user = auth.authenticated(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            context = {"Error": "User not authenticated"}
            return redirect('login')

def edit_course(request, course_id):
    if request.user.is_staff:
        if request.method == "GET":
            context = {
                "course": Course.objects.get(pk=course_id)
            }
            context["course"].start_date = context["course"].start_date.strftime('%Y-%m-%d')
            context["course"].end_date = context["course"].end_date.strftime('%Y-%m-%d')

            return render(request, 'schooltool/edit_course.html', context)

        elif request.method == "POST":
            if request.POST["request"] == "PUT":
                title = request.POST["title"]
                max_students = request.POST["max_students"]
                start_date = request.POST["start_date"]
                end_date = request.POST["end_date"]
                Course.objects.filter(pk=course_id).update(title=title, max_students=max_students, start_date=start_date, end_date=end_date)
                return redirect('/courses/' + course_id + '/edit')
    else:
        return redirect('/courses/' + course_id)

def profile(request):
   context = {"error": False}
   if request.user.is_authenticated:
       return render(request, 'schooltool/secret.html')
   else:
       context["error"] = "Not authenticated"
       return render(request, 'schooltool/signup.html', context)
