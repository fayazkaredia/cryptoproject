from django.shortcuts import render, get_object_or_404, redirect
import requests
import json
import time
from datetime import datetime
from cryptostore.models import Coin, Owns
from .forms import SignUpForm, BuyForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
# Import User UpdateForm, ProfileUpdatForm
from .forms import  UserUpdateForm, ProfileUpdateForm

# Create your views here.


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"


def index(request):
    fetch_data_api()
    coins = Coin.objects.all()
    context = {
        'coins': coins,
        'request': request
    }
    return render(request, 'index.html', context)


def register(request):
    return render(request, 'registration/register.html')


def login(request):
    return render(request, 'registration/login.html')


# def profile(request):
#     if request.user.is_authenticated:
#         coins = []
#         amount = []
#         portfolio = Owns.objects.filter(user=request.user.id)
#         portfolio = portfolio.exclude(quantity=0.0000000000)
#         for i in portfolio:
#             coins.append(i)
#         context = {
#             'username': request.user.username,
#             'first_name': request.user.first_name,
#             'last_name': request.user.last_name,
#             'email': request.user.email,
#             'coins' : coins,
#         }
#         return render(request, 'registration/profile.html', context)
#     else:
#         return redirect('login')

# Update it here
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'registration/profile.html', context)



def detail(request, coin_code):
    coin = get_object_or_404(Coin, coinCode=coin_code)
    form = BuyForm
    url = "https://api.livecoinwatch.com/coins/single/history"
    message = ''

    if request.method == "POST":
        if request.user.is_authenticated:
            form = BuyForm(request.POST)
            if form.is_valid():
                buy_amount = form.cleaned_data['amount']
                own, flag = Owns.objects.get_or_create(user=request.user, coin=coin)
                own.quantity = own.quantity + buy_amount
                own.save()
                message = 'Bought successfully for $ ' + str(coin.coinRate * float(buy_amount))
        else:
            return redirect('login')

    payload = json.dumps({
        "currency": "USD",
        "code": coin.coinCode,
        "start": int(time.time_ns() / 1000000) - 86400000,
        "end": int(time.time_ns() / 1000000),
        "meta": False
    })
    headers = {
        'content-type': 'application/json',
        'x-api-key': 'b5393708-51b0-4254-a7db-fde640feaaeb'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    historyJson = response.json()
    dateList = []
    blackList = []
    priceList = []
    for entry in historyJson['history']:
        d = datetime.utcfromtimestamp(int(entry['date']) / 1000).strftime('%H:%M:%S')
        dateList.append(d)
        blackList.append(entry['date'])
        priceList.append(entry['rate'])

    context = {
        'message' : message,
        'coin': coin,
        'form': form,
        'dateList': dateList,
        'priceList': priceList,
        'blackList': blackList
    }
    if request.user.is_authenticated:
        own, flag = Owns.objects.get_or_create(user=request.user, coin=coin)
        context['owns'] = float(own.quantity)
        context['ownsUSD'] = float(own.quantity) * coin.coinRate
    return render(request, 'detail.html', context)


def buy(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = BuyForm(request.POST)
            buy_amount = form['amount']
            Owns.objects.get_or_create()
        else:
            return redirect('login')


def about(request):
    return render(request, 'about.html', {})


def fetch_data_api():
    urlList = "https://api.livecoinwatch.com/coins/list"
    # https://livecoinwatch.github.io/lcw-api-docs/#coinssingle

    payloadList = json.dumps({
        "currency": "USD",
        "sort": "rank",
        "order": "ascending",
        "offset": 0,
        "limit": 50,
        "meta": True
    })

    headers = {
        'content-type': 'application/json',
        'x-api-key': 'b5393708-51b0-4254-a7db-fde640feaaeb'
    }
    responseList = requests.request("POST", urlList, headers=headers, data=payloadList)
    for dataJson in responseList.json():
        record, flag = Coin.objects.get_or_create(
            coinCode=dataJson['code']
        )
        record.coinRate = dataJson['rate']
        record.coinName = dataJson['name']
        record.coinCap = dataJson['cap']
        record.coinVolume = dataJson['volume']
        record.coinIcon = dataJson['png64']
        record.save()

    # response = HttpResponse()
    # response.write('Database Successfully Updated!<br>')
    # response.write('<a href = http://127.0.0.1:8000/ >Go Back to index</a>')
    return 0
