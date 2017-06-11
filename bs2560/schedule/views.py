from django.shortcuts import render, redirect
from schedule.models import User, Activity
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as User_id
from django.contrib.auth import authenticate, login


''' if this page has value from form it will creat a user object
	and redirect to it self '''
def home_page(request):
    if request.method == 'POST':
        email = request.POST['login_email']
        password = request.POST['login_password']
        user_name = User_id.objects.get(email=email.lower()).username
        user = authenticate(username=user_name, password=password)
        if user is not None:
            user_pk = User.objects.get(mail=email).pk
            login(request, user)
            return redirect(reverse('schedule:user_page', kwargs={'user_id':user_pk}))
        else:
            return render(request, 'schedule/homepage.html', {'error_messege_login':"email or password was worng"})
    return render(request, 'schedule/homepage.html')

def create_user(request):
    new_email = request.POST['email']
    user_name = request.POST['user_name']
    user_pass = request.POST['password']
    try: # if error that mean dont have any user object which have mail = new mail
        check_user_email = User.objects.get(mail=new_email)
    except: # so make it new one 
        user = User.objects.create(name=user_name, mail=new_email)
        user.save()
        generate_activity_for_first_time_of_user('Monday', user.pk)
        generate_activity_for_first_time_of_user('Tuesday', user.pk)
        generate_activity_for_first_time_of_user('Wednesday', user.pk)
        generate_activity_for_first_time_of_user('Thursday', user.pk)
        generate_activity_for_first_time_of_user('Friday', user.pk)
        generate_activity_for_first_time_of_user('Saturday', user.pk)
        generate_activity_for_first_time_of_user('Sunday', user.pk)
        new_id = User_id.objects.create_user(user_name,
                                             new_email,
                                             user_pass)
        new_id.save()
        return redirect(reverse('schedule:home_page'))
    return render(request, 'schedule/homepage.html', {'error_messege_new_user':"That email was alerdy used"})

def generate_activity_for_first_time_of_user(day, user_id):
    user = User.objects.get(pk=user_id)
    for count in range(0, 24):
        Activity.objects.create(user=user,
                                time=count,
                                day=day)

@login_required(login_url='/')
def user_page(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'schedule/userpage.html', {'user': user})

@login_required(login_url='/')
def add_new_activity(request, user_id):
    user = User.objects.get(pk=user_id)
    start_time = int(request.POST['start_time'])
    how_many_hour = int(request.POST['how_many_hour'])
    max_time = start_time + how_many_hour
    day_in = request.POST['day_selecter']
    detail_in = request.POST['detail']
    for count_time in range(start_time, max_time):
        activity_filter = Activity.objects.get(user=user,
                                               time=count_time,
                                               day=day_in,)
        if(activity_filter.connected): # if True that mean it should remove old activity first
            reset_same_time_activity_reverse(user_id, count_time, day_in)

        if(activity_filter.detail != ""): # if That True that mean it find head of activity
            reset_same_time_activity_forward(user_id, count_time, day_in, activity_filter.time_left)

        activity_filter.setDetail(detail_in)
        activity_filter.set_time_left(how_many_hour)
        if(count_time == start_time): # if that is first set it head for make colum span
            activity_filter.set_connected(False)
        else:
            activity_filter.set_connected(True)
        how_many_hour = how_many_hour - 1
        activity_filter.save()
    return redirect(reverse('schedule:user_page', args=[user_id],))

def reset_same_time_activity_reverse(user_id, time, day): #count-down to reset
    user = User.objects.get(pk=user_id)
    extend_activity = Activity.objects.get(user=user, time=time, day=day)
    extend_activity.setDetail("")
    extend_activity.set_time_left(0)
    connected_tem = extend_activity.connected
    extend_activity.set_connected(False)
    extend_activity.save()
    if(connected_tem): # first must be True
        if(time > 0):
            time -= 1
            reset_same_time_activity_reverse(user_id, time, day)

def reset_same_time_activity_forward(user_id, time, day, time_left): # count-up to reset by time-left
    user = User.objects.get(pk=user_id)
    extend_activity = Activity.objects.get(user=user, time=time, day=day)
    extend_activity.setDetail("")
    extend_activity.set_time_left(0)
    if(time_left != 0): # first must be False
        extend_activity.set_connected(False)
        extend_activity.save()
        if(time < 23):
            time += 1
            time_left -= 1
            reset_same_time_activity_forward(user_id, time, day, time_left)

def check_has_same_time(user_id, time, day, spend_time):
    user = User.objects.get(pk=user_id)
    extend_activity = Activity.objects.get(user=user, time=time, day=day)
    collide = []
    if(extend_activity.connected):
        collide.append(find_head_from_connected(user_id, time, day))
    for i in range(time, time+spend_time):
        extend_activity = Activity.objects.get(user=user, time=i, day=day)
        if(extend_activity.detail != "" and extend_activity.connected == False):
            collide.append(i)
    return collide

def find_head_from_connected(user_id, time, day):
    user = User.objects.get(pk=user_id)
    extend_activity = Activity.objects.get(user=user, time=time, day=day)
    if(extend_activity.connected):
        return find_head_from_connected(user_id, time-1, day)
    else:
        return time

@login_required(login_url='/')
def confirm_delete(request, user_id):
    user = User.objects.get(pk=user_id)
    start_time = int(request.POST['start_time'])
    how_many_hour = int(request.POST['how_many_hour'])
    day_in = request.POST['day_selecter']
    detail_in = request.POST['detail']
    max_time = start_time + how_many_hour
    if(max_time > 24):
        return render(request, 'schedule/userpage.html',
                               {'user': user,
                                'error_messege':"Your select time after 23.00 It cant , please Try another time"})
    collide = check_has_same_time(user_id, start_time, day_in, how_many_hour)
    if(collide == []):
        return add_new_activity(request, user_id)
    return render(request, 'schedule/confirm_add.html',{'user': user,
                                                        'collide_time':collide,
                                                        'day':day_in,
                                                        'start':start_time,
                                                        'how_many_hour':how_many_hour,
                                                        'detail_in':detail_in})