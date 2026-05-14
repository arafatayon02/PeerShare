
from django.shortcuts import render

from django.contrib.auth import get_user_model
User = get_user_model()

def home(request):

    users = User.objects.all()


    return render(
        request,
        'home.html',
        {'users': users}
    )