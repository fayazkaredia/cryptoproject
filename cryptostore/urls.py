from django.contrib import admin
from django.urls import path
import cryptostore.views as views

app_name = 'cryptostore'
urlpatterns = [
    path('update', views.fetch_data_api, name="FetchData"),
    path('', views.index, name="index"),
    path('detail/<str:coin_code>', views.detail, name='detail'),
    path('about', views.about, name='about'),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path('profile/', views.profile, name='profile'),

]