from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="shophome"),
    path("about/", views.about, name="aboutus"),
    path("contact/", views.contact, name="contactus"),
    path("tracker/", views.tracker, name="trackingStatus"),
    path("search/", views.search, name="search"),
    path("checkout/", views.checkout, name="checkout"),
    path("Products/<int:myid>", views.productView, name="ProductView"),
    path('signup/', views.handleSignUp, name="handleSignUp"),
    path('login/', views.handeLogin, name="handleLogin"),
    path('logout/', views.handelLogout, name="handleLogout"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit_profile/", views.edit_profile, name="edit_profile"),
]
