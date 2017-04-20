from django.shortcuts import render, redirect
from schedule.models import User, Activity


''' if this page has value from form it will creat a user object 
	and redirect to it self '''
def home_page(request):
    if request.method == 'POST': 
        User.objects.create(name=request.POST['user_name'])
        return redirect('/')
    user_list = User.objects.all()
    return render(request, 'schedule/homepage.html', {'user_list': user_list})

def user_page(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        start_time = int(request.POST['start_time'])
        how_many_hour = int(request.POST['how_many_hour'])
        max_time = start_time + how_many_hour
        for count_time in range(start_time, max_time):
            new_activity = Activity.objects.create(user=user,
                                                   detail=request.POST['detail'],
                                                   time=count_time,
                                                   day=request.POST['day_selecter'])
            new_activity.save()
        return redirect('/%d'%user.pk)
    return render(request, 'schedule/userpage.html', {'user': user})