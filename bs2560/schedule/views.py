from django.shortcuts import render, redirect
from schedule.models import User, Activity


''' if this page has value from form it will creat a user object 
	and redirect to it self '''
def home_page(request):
    if request.method == 'POST': 
        user = User.objects.create(name=request.POST['user_name'])
        user.save()
        generate_activity_for_first_time_of_user('Monday', user.pk)
        generate_activity_for_first_time_of_user('Tuesday', user.pk)
        generate_activity_for_first_time_of_user('Wednesday', user.pk)
        generate_activity_for_first_time_of_user('Thursday', user.pk)
        generate_activity_for_first_time_of_user('Friday', user.pk)
        generate_activity_for_first_time_of_user('Saturday', user.pk)
        generate_activity_for_first_time_of_user('Sunday', user.pk)
        return redirect('/')
    user_list = User.objects.all()
    return render(request, 'schedule/homepage.html', {'user_list': user_list})

def generate_activity_for_first_time_of_user(day, user_id):
    user = User.objects.get(pk=user_id)
    for count in range(0, 24):
        Activity.objects.create(user=user,
                                detail="",
                                time=count,
                                day=day)

def user_page(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        start_time = int(request.POST['start_time'])
        how_many_hour = int(request.POST['how_many_hour'])
        max_time = start_time + how_many_hour
        day_in = request.POST['day_selecter']
        detail_in = request.POST['detail']
        for count_time in range(start_time, max_time):
            activity_filter = Activity.objects.get(user=user, time=count_time, day=day_in)
            activity_filter.setDetail(detail_in)
            activity_filter.save()
        return redirect('/%d'%user.pk)
    return render(request, 'schedule/userpage.html', {'user': user})