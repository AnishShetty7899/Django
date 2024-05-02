from django.shortcuts import render, redirect
from .models import Gadmin
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.
def admin_1(request):
    # if the method in a form is post @ admin.html
    if request.method == 'POST':
        # the value inside a get is given according to html 'name' in admin.htm
        app_icon = request.FILES.get('app_icon') # allocate  a uploded image file to app_icon
        app_name = request.POST.get('app_name') #allocate a app name to app_name
        app_link = request.POST.get('app_link') #allocate a app link to app_link
        app_category = request.POST.get('app_category') #allocate a app category to app_category
        sub_category = request.POST.get('sub_category') #allocate a app sub catagory to sub_category
        points = request.POST.get('points') #allocate a points for the app to points

        # allocateing each value from above var to the db named Gadmin
        # Gadmin values is added to variable 'app'
        acess = Gadmin(app_icon=app_icon, app_name=app_name, app_link=app_link, app_category=app_category, sub_category=sub_category, points=points)

        # and app is used to update the db Gadmin using save
        acess.save()

        # it will display a admin tab
        return render(request, 'admin.html')
    else:
        # it will display a admin tab
        return render(request, 'admin.html')


def index(request):
    # it will give index tab like lochalhost/index
    return render(request, 'index.html')


def register(request):
    # if the method in a form is post @ register.html
    if request.method == 'POST':
        # the value inside a POST is given according to html 'name' in register.html
        first_name = request.POST['f_name'] # allocating the first name of user to first_name variable
        last_name = request.POST['l_name'] # allocating the last name of user to last_name variable
        username = request.POST['u_name'] # allocating the username of user to username variable
        email = request.POST['email'] # allocating the email of user to email variable
        password = request.POST['pass1'] # allocating password  which created by user to password variable
        confirm_password = request.POST['confirm_pass'] # allocating the confirmed password by user to confirm_password variable


        # now verifing that entred password and reentred password for conformation matches or not
        if password == confirm_password:
            # used to check weather that you entred user name is alredy exixt or not
            if User.objects.filter(username=username).exists(): # if yes display the given msg bellow
                messages.info(request, 'The Username already exists! ')
                return redirect('register') # redirect to register tab to enter details again
            # used to check weather that you entred email is alredy exixt or not
            elif User.objects.filter(email=email).exists(): # if yes display the given msg bellow
                messages.info(request, 'The email already exist,try to login!')
                return redirect('register') # redirect to register tab to enter details again

        # when our given values are unique
            else:
                # entred values are allocated to check variable
                check = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                check.save() # it will update registration db
                messages.info(request, 'Registration Completed Successful 🥳')
                return redirect('register') # redirect to register tab to enter new details
        # if there is no match in password
        else:
            messages.info(request, "The password doesn't match")
            return redirect('register') # redirect to register tab to enter details again

 # no post method is done just reloding  register tab
    else:
        return render(request, 'register.html')


def login(request):
    # if the method in a form is post @ login.html
    if request.method == 'POST':
        # the value inside a POST is given according to html 'name' in login.html
        username = request.POST['u_name'] # allocating the username of user to username variable
        password = request.POST['pass1'] # allocating password  which given by  user to password variable

        # it will authenticate the username and password in db and returns a user object to check varible or else give 'None'
        check = auth.authenticate(username=username, password=password)

        # checking weather auth given is none or object
        if check is not None:
            auth.login(request, check) # this function is used in Django to log in a user after they have been successfully authenticated
            messages.info(request, 'Login Successful 🥳')
            return render(request, 'home.html') #after login home tab will open

        # if its None
        else:
            messages.info(request, 'Invalid Username or Password')
            return render(request, 'login.html') # login page will open to re enter values
    # if post method is missing in html form @ login.html
    else:
        return render(request, 'login.html')