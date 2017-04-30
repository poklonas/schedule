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
        if(max_time > 24):
            return render(request, 'schedule/userpage.html', {'user': user, 'error_messege':"Your select time after 23.00 It cant , please Try another time"})
        for count_time in range(start_time, max_time):
            activity_filter = Activity.objects.get(user=user,
                                                   time=count_time,
                                                   day=day_in,)
            if(activity_filter.connected): # if True that mean it should remove old activity first
                reset_same_time_activity_reverse(user_id, count_time, day_in)

            if(activity_filter.detail != ""): # if That True that mean it find head of activity
                reset_same_time_activity_forward(user_id, count_time, day_in)

            activity_filter.setDetail(detail_in)
            if(count_time == start_time): # if that is first set it head for make colum span
                activity_filter.set_time_left(how_many_hour)
                activity_filter.set_connected(False)
            else:
                activity_filter.set_time_left(how_many_hour)
                activity_filter.set_connected(True)
            how_many_hour = how_many_hour - 1
            activity_filter.save()
        return redirect('/%d'%user.pk)
    return render(request, 'schedule/userpage.html', {'user': user})

def reset_same_time_activity_reverse(user_id, time, day): #count-down to reset 
    user = User.objects.get(pk=user_id)
    extend_activity = Activity.objects.get(user=user, time=time, day=day)
    extend_activity.setDetail("")
    extend_activity.set_time_left(0)
    if(extend_activity.connected): # first must be True
        extend_activity.set_connected(False)
        extend_activity.save()
        if(time > 0):
            time -= 1
            reset_same_time_activity_reverse(user_id, time, day)
    else:
        extend_activity.set_connected(False)
        extend_activity.save()

def reset_same_time_activity_forward(user_id, time, day): # count-up to reset by time-left
    user = User.objects.get(pk=user_id)
    extend_activity = Activity.objects.get(user=user, time=time, day=day)
    extend_activity.setDetail("")
    extend_activity.set_time_left(0)
    if(extend_activity.connected): # first must be False 
        extend_activity.set_connected(False)
        extend_activity.save()
    else: 
        extend_activity.set_connected(False)
        extend_activity.save()
        if(time < 23):
            time += 1
            reset_same_time_activity_forward(user_id, time, day)
