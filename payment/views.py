from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def BasketView(request):
    return render(request, 'payment/home.html')