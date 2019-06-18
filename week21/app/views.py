from django.shortcuts import render

# Create your views here.

def tp1(request):
    userlist=[1,2,3]
    return render(request,'tp1.html',{'u':userlist})

def tp2(request):
    name='filter'
    arg='this is a test text'
    return render(request,'tp2.html',{'name':name,'arg':arg})