from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt
from .models import User

def loginHomepage(request):
    return render(request, 'login_registration/loginHomepage.html')

def registration(request):
    print(request.POST['birthday'])
    #pass the post data to the method we wrote and save the response in a variable called errors
    try:
        errors = User.objects.registration_validator(request.POST)
        #check if the errors dictionary has anything in it
        if len(errors) > 0:
            #if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
            #redirect the user back to the form to fix the errors
            return redirect('/login_registration')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], birthday=request.POST['birthday'], email=request.POST['email'], password=pw_hash)

        request.session['user_id'] = user.id

        return redirect('/login_registration/success')
    except:
        return redirect(r'https://www.youtube.com/watch?v=u9Dg-g7t2l4')

def login(request):

    errors = User.objects.login_validator(request.POST)
    user = User.objects.filter(email=request.POST['email'])
    logged_user = user[0]

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login_registration')
    
    else:
        request.session['user_id'] = logged_user.id

    return redirect('/login_registration/success')


def successfulLogin(request):

    if "user_id" not in request.session:
        return redirect('/login_registration')

    context = {
        "user" : User.objects.get(id=request.session['user_id'])
    }
    
    return render(request, 'login_registration/successfulLogin.html', context)
        
def logout(request):
    request.session.clear()
    return redirect('/login_registration')