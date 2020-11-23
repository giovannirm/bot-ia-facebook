from django.shortcuts import render, redirect

def home(request):
    return render(request,'home.html')

def login(request):    
    if request.method =='POST':                
        user = request.POST['user']
        password = request.POST['password']
        if user == 'admin' and password == 'admin':
            return redirect('home')
        else:
            return redirect('login')
    return render(request,'login.html')