from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('contact/', views.contact),
    path('about/', views.about),
    path('contact-us-functionality/', views.send_mail),
    path('login/',views.login),
    path('thankyou/',views.thankyou),
    path('logout/',views.logout),
    path('verifyotp/',views.validate_otp),
    path('signup/',views.Signup.as_view()),
    path('dashboard/',views.Dashboard.as_view()),
    path('dashboard/<pk>',views.UpdateCredential),
    path('dashboard/delete/<pk>',views.DeleteCredential.as_view()),
    path('account/',views.account),
    path('deletemyaccount/',views.accountDelete),
]
