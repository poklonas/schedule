from django.shortcuts import render, redirect
from schedule.models import User

def home_page(request):
    if request.method == 'POST':
        User.objects.create(name=request.POST['user_name'])
        return redirect('/')
    user_list = User.objects.all()
    return render(request, 'schedule/homepage.html', {'user_list': user_list})
