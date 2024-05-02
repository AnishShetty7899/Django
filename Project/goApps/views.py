from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from goApps.models import GoApps
from gApp_Admin.models import Gadmin
from django.http import HttpResponseBadRequest


# Create your views here.


def index(request):
    # it will give index tab like lochalhost/index
    return render(request, 'index.html')


def register(request):
    # if the method in a form is post @ register.html
    if request.method == 'POST':
        # the value inside a POST is given according to html 'name' in register.html
        first_name = request.POST['f_name']  # allocating the first name of user to first_name variable
        last_name = request.POST['l_name']  # allocating the last name of user to last_name variable
        username = request.POST['u_name']  # allocating the username of user to username variable
        email = request.POST['email']  # allocating the email of user to email variable
        password = request.POST['pass1']  # allocating password  which created by user to password variable
        confirm_password = request.POST[
            'confirm_pass']  # allocating the confirmed password by user to confirm_password variable

        # now verifing that entred password and reentred password for conformation matches or not
        if password == confirm_password:
            # used to check weather that you entred username is alredy exixt or not
            if User.objects.filter(username=username).exists():  # if yes display the given msg bellow
                messages.info(request, 'The Username already exists! ')
                return redirect('register')  # redirect to register tab to enter details again
            # used to check weather that you entred email is alredy exixt or not
            elif User.objects.filter(email=email).exists():  # if yes display the given msg bellow
                messages.info(request, 'The email already exist,try to login!')
                return redirect('register')  # redirect to register tab to enter details again

            # when our given values are unique
            else:
                # entred values are allocated to check variable
                check = User.objects.create_user(username=username, password=password, email=email,
                                                 first_name=first_name, last_name=last_name)
                check.save()  # it will update registration db
                messages.info(request, 'Registration Completed Successful 🥳')
                return redirect('register')  # redirect to register tab to enter new details
        # if there is no match in password
        else:
            messages.info(request, "The password doesn't match")
            return redirect('register')  # redirect to register tab to enter details again
    # no post method is done just reloding  register tab
    else:
        return render(request, 'register.html')


def login(request):
    # if the method in a form is post @ login.html
    if request.method == 'POST':
        # the value inside a POST is given according to html 'name' in login.html
        username = request.POST['u_name']  # allocating the username of user to username variable
        password = request.POST['pass1']  # allocating password  which given by  user to password variable

        # it will authenticate the username and password in db and returns a user object to check varible or else give 'None'
        check = auth.authenticate(username=username, password=password)

        # checking weather auth given is none or object
        if check is not None:
            auth.login(request,
                       check)  # this function is used in Django to log in a user after they have been successfully authenticated
            messages.info(request, 'Login Successful 🥳')
            return render(request, 'home.html')  # after login home tab will open

        # if its None
        else:
            messages.info(request, 'Invalid Username or Password')
            return render(request, 'login.html')  # login page will open to re enter values
    # if post method is missing in html form @ login.html
    else:
        return render(request, 'login.html')


def home(request):
    # checks if the current user is authenticated,if yes then loged in and the view proceeds to fetch and display the list of apps.
    if request.user.is_authenticated:
        apps = Gadmin.objects.all()  # It retrieves all objects (apps) from the Gadmin model
        return render(request, 'home.html',
                      {'apps': apps})  # it renders the home.html template, passing the fetched apps as context
    else:
        return redirect('/')  # If the user is not authenticated, the view redirects them to the index.html


def logout(request):
    auth.logout(request)  # it will log out authenticated user
    return redirect('/')  # goes to index.html


@login_required
def App(request, id):
    try:
        app = Gadmin.objects.get(id=id)  # Get the requested app
    except Gadmin.DoesNotExist:
        return HttpResponseBadRequest(
            "App does not exist")  # Handle the case where the app with the given id does not exist

    if request.method == 'POST':
        img = request.FILES.get('img')
        if img:
            # Handle file upload
            # Save the file to a specific location
            with open('img', 'wb+') as destination:
                for chunk in img.chunks():
                    destination.write(chunk)
            # Now you can save the file path to your database
            img_path = 'img'
        else:
            img_path = None
        app_name = request.POST.get('app_name')

        # Check if app_name is provided
        if not app_name:
            return HttpResponseBadRequest("App name is required")

        points = request.POST.get('points')

        # Create and save the GoApps instance
        goapps = GoApps(app_name=app_name, points=points, img=img)
        goapps.save()

        return render(request, 'App.html', {'app': app, 'img': img})

    return render(request, 'App.html', {'app': app})

@login_required
def points(request):
    total_apps = [p for p in GoApps.objects.all()]  # it collect list of app details from GoApps model

    total_points = 0  # initial total points

    app_points = []  # initial app_points list
    app_names = []  # initial app list
    for p in total_apps:  # it will ittrate every app one by one from list
        total_points = total_points + p.points  # adds a initial total point with a points extracted from the list in total_apps var which is extracted from GoApps model
        app_points.append(p.points)  # points from total_app gets appended
        app_names.append(p.app_name)  # also append app name where points refers too
    # it will render points.html temp which appears only mentioned context
    return render(request, 'points.html',
                  {'total_points': total_points, 'app_points': app_points, 'app_names': app_names})


@login_required
def task(request):
    total_apps = [p for p in GoApps.objects.all()]  # it collect list of app details from GoApps model
    app_names = []  # initial app list

    for p in total_apps:
        app_names.append(p.app_name)  # fetch and append app one by one from total_apps
    # it will render task.html temp which appears only mentioned context
    return render(request, 'task.html', {'app_names': app_names})


@login_required
def profile(request):
    user = request.user  # Get the current logged-in user
    return render(request, 'profile.html',{'user': user})  # it will render profile.html
