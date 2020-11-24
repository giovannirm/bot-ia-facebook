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

def add_disease(request):
    return render(request,'add_disease.html')

def update_disease(request):
    pass

def delete_disease(request):
    pass

def read_diseases(request):
    return render(request,'diseases.html')