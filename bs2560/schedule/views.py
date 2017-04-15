from django.shortcuts import render, redirect
from schedule.models import User


''' if this page has value from form it will creat a user object 
	and redirect to it self '''
def home_page(request):
    if request.method == 'POST': 
        User.objects.create(name=request.POST['user_name'])
        return redirect('/')
    user_list = User.objects.all()
    return render(request, 'schedule/homepage.html', {'user_list': user_list})
