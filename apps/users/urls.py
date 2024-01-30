from django.urls import path
from apps.users.views import ContactDetailView, ContactListView, UserLoginView, UserSignupView

urlpatterns = [
	path('contacts/<int:userId>', ContactListView.as_view(), name='contactList'),
	path('login', UserLoginView.as_view(), name='login'),
	path('signup', UserSignupView.as_view(), name='signup'),
]
