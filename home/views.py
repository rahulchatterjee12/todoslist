from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as login_main, logout as logout_main
from project import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes , force_str
from .tokens import generate_token
from django.core.mail.message import EmailMessage
from django.utils.http import urlsafe_base64_encode ,urlsafe_base64_decode
from home.models import ToDo


def home(request):
    return render(request, 'home.html')


def login(request):
    print("in log in page ")
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        user: User = authenticate(request, username=username, password=pass1)
        if user is not None:
            login_main(request, user)
            messages.success(request,"you are loged in")
            fname = user.get_full_name()
            return redirect('home')
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('login.html')
    return render(request, 'login.html')


def register(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request,"Username already exist! try another one")
            return redirect('register')

        if User.objects.filter(email=email):
            messages.error(request,"email id already exist! try another one")
            return redirect('register')
        if pass1 != pass2:
            messages.error(request,"Password not mach")
            return redirect('register')
        if not username.isalnum():
            messages.error(request,"Username must be Alfa-Numeric!")
            return redirect('register')

        #wewlcome email
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your account has been created.")

        subject = "Welcome to To-Do's-List web application"
        message ="Hello! "+ myuser.first_name +".\n " + "We are glad to have you hear.\nThank you for joinning with us.\nHave a nice day"+"\nWe have also sent you a conformation email. please verify your accunt to activate your accunt.\nThank you from Rahul Chatterjee"
        from_email = settings.EMAIL_HOST_USER
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [myuser.email, ]
        send_mail( subject, message, email_from, recipient_list )
        # to_list=[myuser.email]
        # send_mail(subject,message,from_email,to_list,fail_silently=True)


        current_site = get_current_site(request)
        email_subject = "Conformation Email For To-Do's-List"
        email_message = render_to_string('email_conformation.html',{
            'name':myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        email=EmailMessage(
            email_subject ,
            email_subject,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        
        from_email = settings.EMAIL_HOST_USER
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [myuser.email, ]
        send_mail( email_subject, email_message, email_from, recipient_list )
        return redirect('home')

    return render(request, 'register.html')



def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token) :
        myuser.is_active = True
        myuser.save()
        login_main(request,myuser)
        messages.success(request,"Your account is now activated")
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')

def logout(request):
    logout_main(request)
    messages.success(request, "You are loged out")
    return redirect('home')


def addtask(request):
    if request.method == 'POST':
        title = request.POST['title']
        info = request.POST['info']
        date = request.POST['date']
        myuser =request.user
        ins = ToDo(user=myuser,title=title,info=info,date=date)
        ins.save()
        messages.success(request,"Your task is successfully added")
    return render(request, 'task.html')


def tasklist(request):
    myuser = request.user
    allTasks = ToDo.objects.all().filter(user=myuser)
    context = {'tasks': allTasks}
    return render(request, 'tasklist.html',context)

def edit(request,task_id):
    if request.method=='POST':
        new_title = request.POST['title']
        new_info = request.POST['info']
        new_date = request.POST['date']
        task = ToDo.objects.get(id= task_id)
        myuser =request.user
        
        task.title = new_title
        task.info = new_info
        task.date = new_date
        task.save()
        messages.success(request, "Your Task Updated Successfully.")
        return redirect('tasklist')
    task =ToDo.objects.get(id= task_id)  
    context = {'title': task.title,'info':task.info,'date':task.date ,'id':task.id}
    return render(request,'edit.html',context)


def delete(request,task_id):
    if request.method=='POST':
        task = ToDo.objects.get(id= task_id)
        task.delete()
        messages.success(request, "Your task deleted successfully.")
        return redirect('tasklist')

    task = {"task":ToDo.objects.get(id = task_id)}    
    return render(request, 'delete.html',task)


def about(request):
    return render(request, 'about.html')
