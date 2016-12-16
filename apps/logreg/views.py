from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages

# Create your views here.
def index(request):
    if "logged_user"  in request.session:
        return redirect('/success')
    return render(request, 'logreg/index.html')
def success(request):
    if "logged_user" not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['logged_user'])
    return render(request, 'logreg/success.html', {"user":user})

def signout(request):
    request.session.pop('logged_user', None)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        form = request.POST
        #replace view/controller code with model code
        errors = User.objects.validate_registration(form)

        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            #if we make it to this else then we want to register
            #replace view/controller code with model code
            if User.objects.register(form):
                messages.success(request, "You have successfully created an account, please login to continue")
            else:
                messages.error(request, "something went wrong")
    return redirect('/')


def login(request):
    if request.method != "POST":
        return redirect('/')

    user = User.objects.check_login(request.POST)
    if user:
        #here we attach to session and proceed to success page
        messages.success(request, 'Successful Login')
        request.session['logged_user'] = user.id
        return redirect('/success')
    else:
        messages.error(request, 'Invalid login credentials')
        return redirect('/')
    #otherwise, we can do our work:
